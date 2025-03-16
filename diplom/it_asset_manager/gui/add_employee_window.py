import tkinter as tk
from tkinter import ttk, messagebox
from models.employee import Employee

class AddEmployeeWindow(tk.Toplevel):
    def __init__(self, parent, db_connector, refresh_callback):
        super().__init__(parent)
        self.parent = parent
        self.db_connector = db_connector
        self.refresh_callback = refresh_callback
        self.title("Добавить сотрудника")
        self.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Имя сотрудника:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Должность:").grid(row=1, column=0, padx=5, pady=5)
        self.position_entry = tk.Entry(self)
        self.position_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_employee)
        self.add_button.grid(row=2, column=1, padx=5, pady=5)

    def add_employee(self):
        """Добавляет нового сотрудника в базу данных."""
        try:
            name = self.name_entry.get()
            position = self.position_entry.get()

            if not name:
                messagebox.showerror("Ошибка", "Введите имя сотрудника.")
                return
            if not position:
                messagebox.showerror("Ошибка", "Введите должность сотрудника.")
                return

            new_employee = Employee(name=name, position=position)
            self.db_connector.insert_employee(new_employee)
            messagebox.showinfo("Успех", "Сотрудник успешно добавлен!")
            self.refresh_callback()  # Обновляем список сотрудников в главном окне (если это нужно)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении сотрудника: {e}")