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
        main_window = MainWindow(root, db_connector)  # Pass only root and db_connector
        root.mainloop()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'db_connector' in locals() and db_connector:
            db_connector.disconnect()

