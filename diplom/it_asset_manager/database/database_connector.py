import sqlite3
from models.device import Device
from models.department import Department
from models.employee import Employee
from tkinter import messagebox

class DatabaseConnector:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()  # Создаем все таблицы

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print("Connected to SQLite")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            messagebox.showerror("Ошибка", f"Ошибка подключения к базе данных: {e}")
            raise

    def disconnect(self):
        if self.conn:
            try:
                self.cursor.close()
            except sqlite3.Error:
                pass
            try:
                self.conn.close()
            except sqlite3.Error:
                pass
            print("Disconnected from SQLite")

    def create_tables(self):
        self.create_departments_table()
        self.create_employees_table()
        self.create_devices_table()

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
                    purchase_date TEXT,  -- Добавлено
                    FOREIGN KEY (department_id) REFERENCES departments(id),
                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                )
            """)
            self.connection.commit()
            print("Table created (if it didn't exist)")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_devices_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category TEXT,
                    serial_number TEXT,
                    status TEXT,
                    purchase_date TEXT,
                    warranty_until TEXT,
                    description TEXT,
                    department_id INTEGER,
                    employee_id INTEGER,
                    FOREIGN KEY (department_id) REFERENCES departments (id),
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            """)
            self.conn.commit()
            print("Table 'devices' created (if it didn't exist)")
        except sqlite3.Error as e:
            print(f"Error creating table 'devices': {e}")
            messagebox.showerror("Ошибка", f"Ошибка при создании таблицы 'devices': {e}")
            if self.conn:
                self.conn.rollback()
            raise
    # Методы для работы с departments
    def insert_department(self, department):
        try:
            self.cursor.execute("""
                INSERT INTO departments (name)
                VALUES (?)
            """, (department.name,))
            self.conn.commit()
            department.id = self.cursor.lastrowid # Получаем ID вставленного отдела
            print(f"Department '{department.name}' inserted successfully")
        except sqlite3.Error as e:
            print(f"Error inserting department: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при добавлении отдела: {e}")
            if self.conn:
                self.conn.rollback()
            raise

    def fetch_all_departments(self):
        try:
            self.cursor.execute("SELECT * FROM departments")
            rows = self.cursor.fetchall()
            departments = []
            for row in rows:
                department = Department(id=row[0], name=row[1])
                departments.append(department)
            return departments
        except sqlite3.Error as e:
            print(f"Error fetching departments: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при чтении отделов: {e}")
            return []

    # Методы для работы с employees
    def insert_employee(self, employee):
      try:
          self.cursor.execute("""
              INSERT INTO employees (name, position)
              VALUES (?, ?)
          """, (employee.name, employee.position))
          self.conn.commit()
          employee.id = self.cursor.lastrowid
          print(f"Employee '{employee.name}' inserted successfully")
      except sqlite3.Error as e:
          print(f"Error inserting employee: {e}")
          messagebox.showerror("Ошибка", f"Ошибка при добавлении сотрудника: {e}")
          if self.conn:
              self.conn.rollback()
          raise

    def fetch_all_employees(self):
        try:
            self.cursor.execute("SELECT * FROM employees")
            rows = self.cursor.fetchall()
            employees = []
            for row in rows:
                employee = Employee(id=row[0], name=row[1], position=row[2])
                employees.append(employee)
            return employees
        except sqlite3.Error as e:
            print(f"Error fetching employees: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при чтении сотрудников: {e}")
            return []
    # Методы для работы с devices
    def insert_device(self, device):
        try:
            self.cursor.execute("""
                INSERT INTO devices (name, category, serial_number, status, purchase_date, warranty_until, description, department_id, employee_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (device.name, device.category, device.serial_number, device.status,
                  str(device.purchase_date), str(device.warranty_until), device.description, device.department_id, device.employee_id))
            self.conn.commit()
            print(f"Device '{device.name}' inserted successfully")
        except sqlite3.Error as e:
            print(f"Error inserting device: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при добавлении устройства: {e}")
            if self.conn:
                self.conn.rollback()
            raise

    def fetch_all_devices(self):
        try:
            self.cursor.execute("""
                SELECT devices.id, devices.name, devices.category, devices.serial_number, devices.status,
                       devices.purchase_date, devices.warranty_until, devices.description,
                       departments.name AS department_name, employees.name AS employee_name
                FROM devices
                LEFT JOIN departments ON devices.department_id = departments.id
                LEFT JOIN employees ON devices.employee_id = employees.id
            """)
            rows = self.cursor.fetchall()
            devices = []
            for row in rows:
                device = Device(id=row[0], name=row[1], category=row[2], serial_number=row[3],
                                status=row[4], purchase_date=row[5], warranty_until=row[6],
                                description=row[7], department_id=row[8], employee_id=row[9])  # department_id и employee_id теперь в Device
                devices.append(device)
            return devices
        except sqlite3.Error as e:
            print(f"Error fetching devices: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при чтении устройств: {e}")
            return []
    def update_device(self, device):
        try:
            self.cursor.execute("""
                UPDATE devices
                SET name=?, category=?, serial_number=?, status=?, purchase_date=?, warranty_until=?,
                    description=?, department_id=?, employee_id=?
                WHERE id=?
            """, (device.name, device.category, device.serial_number, device.status,
                  str(device.purchase_date), str(device.warranty_until), device.description,
                  device.department_id, device.employee_id, device.id))
            self.conn.commit()
            print(f"Device with id {device.id} updated successfully")
        except sqlite3.Error as e:
            print(f"Error updating device: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при обновлении устройства: {e}")
            if self.conn:
                self.conn.rollback()
            raise

    def delete_device(self, device_id):
        try:
            self.cursor.execute("DELETE FROM devices WHERE id = ?", (device_id,))
            self.conn.commit()
            print(f"Device with id {device_id} deleted successfully")
        except sqlite3.Error as e:
            print(f"Error deleting device: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при удалении устройства: {e}")
            if self.conn:
                self.conn.rollback()
            raise

def delete_department(self, department_id):
    try:
        self.cursor.execute("DELETE FROM departments WHERE id = ?", (department_id,))
        self.conn.commit()
        print(f"Department with id {department_id} deleted successfully")
    except sqlite3.Error as e:
        print(f"Error deleting department: {e}")
        if self.conn:
            self.conn.rollback()
        raise

def check_if_department_has_devices(self, department_id):
    try:
        self.cursor.execute("SELECT COUNT(*) FROM devices WHERE department_id = ?", (department_id,))
        count = self.cursor.fetchone()[0]
        return count > 0
    except sqlite3.Error as e:
        print(f"Error checking for devices in department: {e}")
        return True  # Возвращаем True, чтобы предотвратить удаление в случае ошибки

def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.populate_departments() # Добавляем заполнение отделов

def populate_departments(self):
        """Заполняет таблицу departments стандартными отделами, если она пуста."""
        if not self.fetch_all_departments():  # Проверяем, есть ли отделы
            departments = [
                Department(name="Материальный отдел"),
                Department(name="Расчётный отдел"),
                Department(name="Договорный отдел"),
                Department(name="Отдел банковских и кассовых операций"),
                Department(name="Экономический отдел"),
                Department(name="Отдел технического обеспечения")
            ]
            for department in departments:
                self.insert_department(department)
            print("Стандартные отделы добавлены в базу данных.")

def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.populate_departments()
        self.populate_employees() # Добавляем заполнение сотрудников

def populate_employees(self):
        """Заполняет таблицу employees стандартными сотрудниками, если она пуста."""
        if not self.fetch_all_employees():  # Проверяем, есть ли сотрудники
            employees = [
                Employee(name="Иванов Иван Иванович", position="Системный администратор"),
                Employee(name="Петров Петр Петрович", position="Бухгалтер"),
                Employee(name="Сидоров Сидор Сидорович", position="Юрист")
            ]
            for employee in employees:
                self.insert_employee(employee)
            print("Стандартные сотрудники добавлены в базу данных.")

def fetch_employees_by_department(self, department_id):
        try:
            # Выбираем сотрудников, у которых employee_id соответствует одному из устройств в данном отделе
            self.cursor.execute("""
                SELECT DISTINCT employees.id, employees.name, employees.position
                FROM employees
                INNER JOIN devices ON employees.id = devices.employee_id
                WHERE devices.department_id = ?
            """, (department_id,))
            rows = self.cursor.fetchall()
            employees = []
            for row in rows:
                employee = Employee(id=row[0], name=row[1], position=row[2])
                employees.append(employee)
            return employees
        except sqlite3.Error as e:
            print(f"Error fetching employees by department: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при чтении сотрудников по отделу: {e}")
            return []
