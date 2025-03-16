import tkinter as tk
from tkinter import ttk, messagebox
from models.device import Device
from models.department import Department
from models.employee import Employee

class AddDepartmentWindow(tk.Toplevel):
    def __init__(self, parent, db_connector, refresh_callback):
        super().__init__(parent)
        self.parent = parent
        self.db_connector = db_connector
        self.refresh_callback = refresh_callback
        self.title("Добавить отдел")
        self.geometry("300x150")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Название отдела:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_department)
        self.add_button.grid(row=1, column=1, padx=5, pady=5)

    def add_department(self):
        """Добавляет новый отдел в базу данных."""
        department_name = self.name_entry.get()
        if department_name:
            if self.db_connector.insert_department(department_name):  # Передаем только имя
                messagebox.showinfo("Успех", "Отдел успешно добавлен.")
                self.load_departments()  # Обновляем список отделов
                self.root.destroy()
            else:
                messagebox.showerror("Ошибка", "Ошибка при добавлении отдела.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите название отдела.")