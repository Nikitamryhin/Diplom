import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

class DatabaseConnector:
    def __init__(self, db_name):
        self.db_name = db_name
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.create_tables()
            print("Database connected successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_tables(self):
        """Создает таблицы, если они не существуют."""
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
                    department_id INTEGER,
                    name TEXT NOT NULL,
                    FOREIGN KEY (department_id) REFERENCES departments (id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    department_id INTEGER,
                    name TEXT NOT NULL,
                    FOREIGN KEY (department_id) REFERENCES departments (id)
                )
            """)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    # --- Отделы ---
    def insert_department(self, name):
        """Вставляет новый отдел в базу данных."""
        try:
            self.cursor.execute("INSERT INTO departments (name) VALUES (?)", (name,))
            self.connection.commit()
            print("Department inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def fetch_all_departments(self):
        """Получает все отделы из базы данных."""
        try:
            self.cursor.execute("SELECT id, name FROM departments")
            departments = self.cursor.fetchall()
            return [{"id": row[0], "name": row[1]} for row in departments]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def delete_department(self, department_id):
        """Удаляет отдел из базы данных."""
        try:
            self.cursor.execute("DELETE FROM departments WHERE id = ?", (department_id,))
            self.connection.commit()
            print("Department deleted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_department(self, department_id, new_name):
        """Обновляет название отдела в базе данных."""
        try:
            self.cursor.execute("UPDATE departments SET name = ? WHERE id = ?", (new_name, department_id))
            self.connection.commit()
            print("Department updated successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    # --- Сотрудники ---
    def insert_employee(self, department_id, name):
        """Вставляет нового сотрудника в базу данных."""
        try:
            self.cursor.execute("INSERT INTO employees (department_id, name) VALUES (?, ?)", (department_id, name))
            self.connection.commit()
            print("Employee inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def fetch_all_employees(self, department_id):
        """Получает всех сотрудников из отдела."""
        try:
            self.cursor.execute("SELECT id, name FROM employees WHERE department_id = ?", (department_id,))
            employees = self.cursor.fetchall()
            return [{"id": row[0], "name": row[1]} for row in employees]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def delete_employee(self, employee_id):
        """Удаляет сотрудника из базы данных."""
        try:
            self.cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            self.connection.commit()
            print("Employee deleted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_employee(self, employee_id, new_name):
         """Обновляет имя сотрудника."""
         try:
             self.cursor.execute("UPDATE employees SET name = ? WHERE id = ?", (new_name, employee_id))
             self.connection.commit()
             print("Employee updated successfully")
         except sqlite3.Error as e:
             print(f"An error occurred: {e}")


    # --- Устройства ---
    def insert_device(self, department_id, name):
        """Вставляет новое устройство в базу данных."""
        try:
            self.cursor.execute("INSERT INTO devices (department_id, name) VALUES (?, ?)", (department_id, name))
            self.connection.commit()
            print("Device inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def fetch_all_devices(self, department_id):
        """Получает все устройства из отдела."""
        try:
            self.cursor.execute("SELECT id, name FROM devices WHERE department_id = ?", (department_id,))
            devices = self.cursor.fetchall()
            return [{"id": row[0], "name": row[1]} for row in devices]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def delete_device(self, device_id):
        """Удаляет устройство из базы данных."""
        try:
            self.cursor.execute("DELETE FROM devices WHERE id = ?", (device_id,))
            self.connection.commit()
            print("Device deleted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_device(self, device_id, new_name):
        """Обновляет имя устройства."""
        try:
            self.cursor.execute("UPDATE devices SET name = ? WHERE id = ?", (new_name, device_id))
            self.connection.commit()
            print("Device updated successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()
            print("Database connection closed")

class MainWindow(tk.Tk):
    def __init__(self, db_connector):
        super().__init__()
        self.db_connector = db_connector
        self.title("Управление отделами, сотрудниками и устройствами")
        self.geometry("800x600")  # Увеличиваем размер окна

        # --- Фреймы ---
        self.department_frame = ttk.LabelFrame(self, text="Отделы")
        self.department_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.employee_frame = ttk.LabelFrame(self, text="Сотрудники")
        self.employee_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.device_frame = ttk.LabelFrame(self, text="Устройства")
        self.device_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # --- Списки ---
        self.department_list = tk.Listbox(self.department_frame)
        self.department_list.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        self.employee_list = tk.Listbox(self.employee_frame)
        self.employee_list.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        self.device_list = tk.Listbox(self.device_frame)
        self.device_list.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # --- Кнопки отделов ---
        self.add_department_button = ttk.Button(self.department_frame, text="Добавить отдел", command=self.add_department)
        self.add_department_button.pack(pady=2, padx=2)
        self.edit_department_button = ttk.Button(self.department_frame, text="Редактировать отдел", command=self.edit_department)
        self.edit_department_button.pack(pady=2, padx=2)
        self.delete_department_button = ttk.Button(self.department_frame, text="Удалить отдел", command=self.delete_department)
        self.delete_department_button.pack(pady=2, padx=2)

        # --- Кнопки сотрудников ---
        self.add_employee_button = ttk.Button(self.employee_frame, text="Добавить сотрудника", command=self.add_employee)
        self.add_employee_button.pack(pady=2, padx=2)
        self.edit_employee_button = ttk.Button(self.employee_frame, text="Редактировать сотрудника", command=self.edit_employee)
        self.edit_employee_button.pack(pady=2, padx=2)
        self.delete_employee_button = ttk.Button(self.employee_frame, text="Удалить сотрудника", command=self.delete_employee)
        self.delete_employee_button.pack(pady=2, padx=2)

       # --- Кнопки устройств ---
        self.add_device_button = ttk.Button(self.device_frame, text="Добавить устройство", command=self.add_device)
        self.add_device_button.pack(pady=2, padx=2)
        self.edit_device_button = ttk.Button(self.device_frame, text="Редактировать устройство", command=self.edit_device)
        self.edit_device_button.pack(pady=2, padx=2)
        self.delete_device_button = ttk.Button(self.device_frame, text="Удалить устройство", command=self.delete_device)
        self.delete_device_button.pack(pady=2, padx=2)

        # --- Переменные ---
        self.selected_department_id = None

        # --- Загрузка данных ---
        self.load_departments()

        # --- Привязка событий ---
        self.department_list.bind("<<ListboxSelect>>", self.on_department_select)

    # --- Функции отделов ---
    def load_departments(self):
        """Загружает отделы из базы данных и отображает их."""
        self.department_list.delete(0, tk.END)
        departments = self.db_connector.fetch_all_departments()
        for department in departments:
            self.department_list.insert(tk.END, f"{department['name']} (ID: {department['id']})")

    def add_department(self):
        """Добавляет новый отдел."""
        name = simpledialog.askstring("Добавить отдел", "Введите название отдела:")
        if name:
            self.db_connector.insert_department(name)
            self.load_departments()

    def edit_department(self):
        """Редактирует выбранный отдел."""
        selected_department = self.department_list.curselection()
        if selected_department:
            selected_department_text = self.department_list.get(selected_department[0])
            department_id = int(selected_department_text.split("(ID: ")[1][:-1])
            new_name = simpledialog.askstring("Редактировать отдел", "Введите новое название отдела:")
            if new_name:
                self.db_connector.update_department(department_id, new_name)
                self.load_departments()
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для редактирования.")

    def delete_department(self):
        """Удаляет выбранный отдел."""
        selected_department = self.department_list.curselection()
        if selected_department:
            selected_department_text = self.department_list.get(selected_department[0])
            department_id = int(selected_department_text.split("(ID: ")[1][:-1])
            self.db_connector.delete_department(department_id)
            self.load_departments()
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для удаления.")

    # --- Функции сотрудников ---
    def load_employees(self, department_id):
        """Загружает сотрудников для выбранного отдела."""
        self.employee_list.delete(0, tk.END)
        employees = self.db_connector.fetch_all_employees(department_id)
        for employee in employees:
            self.employee_list.insert(tk.END, f"{employee['name']} (ID: {employee['id']})")

    def add_employee(self):
        """Добавляет нового сотрудника."""
        if self.selected_department_id:
            name = simpledialog.askstring("Добавить сотрудника", "Введите имя сотрудника:")
            if name:
                self.db_connector.insert_employee(self.selected_department_id, name)
                self.load_employees(self.selected_department_id)
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для добавления сотрудника.")

    def edit_employee(self):
        """Редактирует выбранного сотрудника."""
        selected_employee = self.employee_list.curselection()
        if selected_employee and self.selected_department_id:
            selected_employee_text = self.employee_list.get(selected_employee[0])
            employee_id = int(selected_employee_text.split("(ID: ")[1][:-1])
            new_name = simpledialog.askstring("Редактировать сотрудника", "Введите новое имя сотрудника:")
            if new_name:
                self.db_connector.update_employee(employee_id, new_name)
                self.load_employees(self.selected_department_id)
        else:
            messagebox.showinfo("Внимание", "Выберите сотрудника для редактирования.")

    def delete_employee(self):
        """Удаляет выбранного сотрудника."""
        selected_employee = self.employee_list.curselection()
        if selected_employee and self.selected_department_id:
            selected_employee_text = self.employee_list.get(selected_employee[0])
            employee_id = int(selected_employee_text.split("(ID: ")[1][:-1])
            self.db_connector.delete_employee(employee_id)
            self.load_employees(self.selected_department_id)
        else:
            messagebox.showinfo("Внимание", "Выберите сотрудника для удаления.")

    # --- Функции устройств ---
    def load_devices(self, department_id):
        """Загружает устройства для выбранного отдела."""
        self.device_list.delete(0, tk.END)
        devices = self.db_connector.fetch_all_devices(department_id)
        for device in devices:
            self.device_list.insert(tk.END, f"{device['name']} (ID: {device['id']})")

    def add_device(self):
        """Добавляет новое устройство."""
        if self.selected_department_id:
            name = simpledialog.askstring("Добавить устройство", "Введите имя устройства:")
            if name:
                self.db_connector.insert_device(self.selected_department_id, name)
                self.load_devices(self.selected_department_id)
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для добавления устройства.")

    def edit_device(self):
        """Редактирует выбранное устройство."""
        selected_device = self.device_list.curselection()
        if selected_device and self.selected_department_id:
            selected_device_text = self.device_list.get(selected_device[0])
            device_id = int(selected_device_text.split("(ID: ")[1][:-1])
            new_name = simpledialog.askstring("Редактировать устройство", "Введите новое имя устройства:")
            if new_name:
                self.db_connector.update_device(device_id, new_name)
                self.load_devices(self.selected_department_id)
        else:
            messagebox.showinfo("Внимание", "Выберите устройство для редактирования.")

    def delete_device(self):
        """Удаляет выбранное устройство."""
        selected_device = self.device_list.curselection()
        if selected_device and self.selected_department_id:
            selected_device_text = self.device_list.get(selected_device[0])
            device_id = int(selected_device_text.split("(ID: ")[1][:-1])
            self.db_connector.delete_device(device_id)
            self.load_devices(self.selected_department_id)
        else:
            messagebox.showinfo("Внимание", "Выберите устройство для удаления.")

    # --- Обработчик выбора отдела ---
    def on_department_select(self, event):
        """Обрабатывает выбор отдела в списке."""
        selected_department = self.department_list.curselection()
        if selected_department:
            selected_department_text = self.department_list.get(selected_department[0])
            self.selected_department_id = int(selected_department_text.split("(ID: ")[1][:-1])
            self.load_employees(self.selected_department_id)
            self.load_devices(self.selected_department_id)
        else:
            self.selected_department_id = None
            self.employee_list.delete(0, tk.END)
            self.device_list.delete(0, tk.END)

# --- Запуск приложения ---
if __name__ == "__main__":
    db_name = "departments.db"
    db_connector = DatabaseConnector(db_name)
    app = MainWindow(db_connector)
    app.mainloop()
    db_connector.close()