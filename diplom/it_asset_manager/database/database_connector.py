import sqlite3
import os
from tkinter import messagebox
from models.device import Device
from models.department import Department
from models.employee import Employee

class DatabaseConnector:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None  # Инициализируем атрибут connection
        self.cursor = None
        self.connect()
        self.create_tables()
        self.populate_departments()
        self.populate_employees()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print("Connected to SQLite")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при подключении к базе данных: {e}")

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT,
                    department_id INTEGER,
                    FOREIGN KEY (department_id) REFERENCES departments(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    serial_number TEXT,
                    status TEXT,
                    department_id INTEGER,
                    employee_id INTEGER,
                    purchase_date TEXT,
                    FOREIGN KEY (department_id) REFERENCES departments(id),
                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                )
            """)
            self.connection.commit()
            print("Table created (if it didn't exist)")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def populate_departments(self):
        """Заполняет таблицу departments начальными данными, если она пуста."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM departments")
            count = self.cursor.fetchone()[0]
            if count == 0:
                self.cursor.execute("INSERT INTO departments (name) VALUES (?)", ("Отдел разработки",))
                self.cursor.execute("INSERT INTO departments (name) VALUES (?)", ("Отдел тестирования",))
                self.connection.commit()
                print("Initial departments populated")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def populate_employees(self):
        """Заполняет таблицу employees начальными данными, если она пуста."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM employees")
            count = self.cursor.fetchone()[0]
            if count == 0:
                # Получаем ID отделов разработки и тестирования
                self.cursor.execute("SELECT id FROM departments WHERE name = ?", ("Отдел разработки",))
                development_department_id = self.cursor.fetchone()[0]

                self.cursor.execute("SELECT id FROM departments WHERE name = ?", ("Отдел тестирования",))
                testing_department_id = self.cursor.fetchone()[0]

                # Добавляем сотрудников в отделы
                self.cursor.execute("INSERT INTO employees (name, position, department_id) VALUES (?, ?, ?)",
                                    ("Иванов Иван Иванович", "Системный администратор", development_department_id))
                self.cursor.execute("INSERT INTO employees (name, position, department_id) VALUES (?, ?, ?)",
                                    ("Петров Петр Петрович", "Тестировщик", testing_department_id))
                self.connection.commit()
                print("Initial employees populated")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def fetch_all_devices(self, department_id=None):
        """Получает все устройства из базы данных."""
        try:
            if department_id is None:
                self.cursor.execute("SELECT * FROM devices")
            else:
                sql = """
                    SELECT devices.id, devices.name, devices.category, devices.serial_number, devices.status, departments.name AS department_name, employees.name AS employee_name
                    FROM devices
                    LEFT JOIN departments ON devices.department_id = departments.id
                    LEFT JOIN employees ON devices.employee_id = employees.id
                    WHERE devices.department_id = ?
                """
                self.cursor.execute(sql, (department_id,))

            rows = self.cursor.fetchall()
            devices = []
            for row in rows:
                device = Device(
                    row[0],  # id
                    row[1],  # name
                    row[2],  # category
                    row[3],  # serial_number
                    row[4],  # status
                    row[5],  # department_name
                    row[6]   # employee_name
                )
                devices.append(device)
            return devices
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def fetch_all_employees(self, department_id=None):
        """Получает всех сотрудников из базы данных."""
        try:
            if department_id is None:
                self.cursor.execute("SELECT * FROM employees")
            else:
                self.cursor.execute("SELECT * FROM employees WHERE department_id = ?", (department_id,))

            rows = self.cursor.fetchall()
            employees = []
            for row in rows:
                employee = Employee(row[0], row[1], row[2])
                employees.append(employee)
            return employees
        except sqlite3.Error as e:
            print(f"An error fetching employees: {e}")
            return []

    def fetch_all_departments(self):
        """Получает все отделы из базы данных."""
        try:
            self.cursor.execute("SELECT * FROM departments")
            rows = self.cursor.fetchall()
            departments = [Department(row[0], row[1]) for row in rows]
            return departments
        except sqlite3.Error as e:
            print(f"An error fetching departments: {e}")
            return []

    def insert_device(self, name, category, serial_number, status, department_id, employee_id):
        """Вставляет новое устройство в базу данных."""
        try:
            self.cursor.execute("""
                INSERT INTO devices (name, category, serial_number, status, department_id, employee_id, purchase_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, category, serial_number, status, department_id, employee_id, None))
            self.connection.commit()
            print("Device inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def insert_department(self, name):
        """Вставляет новый отдел в базу данных."""
        try:
            self.cursor.execute("INSERT INTO departments (name) VALUES (?)", (name,))
            self.connection.commit()
            print("Department inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def insert_employee(self, name, position, department_id):
        """Вставляет нового сотрудника в базу данных."""
        try:
            self.cursor.execute("""
                INSERT INTO employees (name, position, department_id)
                VALUES (?, ?, ?)
            """, (name, position, department_id))
            self.connection.commit()
            print("Employee inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_device(self, device_id):
        """Удаляет устройство из базы данных."""
        try:
            self.cursor.execute("DELETE FROM devices WHERE id = ?", (device_id,))
            self.connection.commit()
            print("Device deleted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_department(self, department_id):
        """Удаляет отдел из базы данных."""
        try:
            self.cursor.execute("DELETE FROM departments WHERE id = ?", (department_id,))
            self.connection.commit()
            print("Department deleted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_employee(self, employee_id):
        """Удаляет сотрудника из базы данных."""
        try:
            self.cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            self.connection.commit()
            print("Employee deleted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_device(self, device_id, name, category, serial_number, status, department_id, employee_id):
        """Обновляет информацию об устройстве в базе данных."""
        try:
            self.cursor.execute("""
                UPDATE devices
                SET name = ?, category = ?, serial_number = ?, status = ?, department_id = ?, employee_id = ?
                WHERE id = ?
            """, (name, category, serial_number, status, department_id, employee_id, device_id))
            self.connection.commit()
            print("Device updated successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_department(self, department_id, name):
         """Обновляет информацию об отделе в базе данных."""
         try:
             self.cursor.execute("""
                 UPDATE departments
                 SET name = ?
                 WHERE id = ?
             """, (name, department_id))
             self.connection.commit()
             print("Department updated successfully")
         except sqlite3.Error as e:
             print(f"An error occurred: {e}")

    def update_employee(self, employee_id, name, position, department_id):
        """Обновляет информацию о сотруднике в базе данных."""
        try:
            self.cursor.execute("""
                UPDATE employees
                SET name = ?, position = ?, department_id = ?
                WHERE id = ?
            """, (name, position, department_id, employee_id))
            self.connection.commit()
            print("Employee updated successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()
            print("Disconnected from SQLite")
