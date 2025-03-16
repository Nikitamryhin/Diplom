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
        try:
            name = self.name_entry.get()
            if not name:
                messagebox.showerror("Ошибка", "Введите название отдела.")
                return

            new_department = Department(name=name)
            self.db_connector.insert_department(new_department)
            messagebox.showinfo("Успех", "Отдел успешно добавлен!")
            self.refresh_callback()  # Обновляем список отделов в главном окне (если это нужно)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении отдела: {e}")