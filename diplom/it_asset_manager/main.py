import tkinter as tk
from gui.main_window import MainWindow
from database.database_connector import DatabaseConnector
import os
from models.employee import Employee
if __name__ == "__main__":
    # Путь к базе данных SQLite
    DB_PATH = "devices.db"  # Укажите имя файла базы данных

    try:
        # Создаем подключение к базе данных
        db_connector = DatabaseConnector(DB_PATH)
        db_connector.connect()

        # Создаем главное окно приложения
        root = tk.Tk()
        main_window = MainWindow(root, db_connector)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'db_connector' in locals() and db_connector:
            db_connector.disconnect()

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