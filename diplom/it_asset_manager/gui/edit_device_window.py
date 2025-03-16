import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from models.device import Device
from models.department import Department
from models.employee import Employee

class EditDeviceWindow(tk.Toplevel):
    def __init__(self, parent, db_connector, device, refresh_callback):
        super().__init__(parent)
        self.parent = parent
        self.db_connector = db_connector
        self.device = device
        self.refresh_callback = refresh_callback
        self.title("Редактировать устройство")
        self.geometry("400x400")  # Увеличиваем высоту окна
        self.departments = []
        self.employees = []
        self.create_widgets()
        self.load_departments_and_employees()
        self.populate_fields()

    def create_widgets(self):
        # Labels и Entry для ввода данных устройства (как и раньше)
        tk.Label(self, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(self)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Серийный номер:").grid(row=2, column=0, padx=5, pady=5)
        self.serial_number_entry = tk.Entry(self)
        self.serial_number_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Статус:").grid(row=3, column=0, padx=5, pady=5)
        self.status_entry = tk.Entry(self)
        self.status_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Дата покупки (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
        self.purchase_date_entry = tk.Entry(self)
        self.purchase_date_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="Гарантия до (YYYY-MM-DD):").grid(row=5, column=0, padx=5, pady=5)
        self.warranty_until_entry = tk.Entry(self)
        self.warranty_until_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self, text="Описание:").grid(row=6, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=6, column=1, padx=5, pady=5)

        # Добавляем выпадающие списки для выбора отдела и сотрудника
        tk.Label(self, text="Отдел:").grid(row=7, column=0, padx=5, pady=5)
        self.department_combobox = ttk.Combobox(self, values=[])
        self.department_combobox.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self, text="Ответственный сотрудник:").grid(row=8, column=0, padx=5, pady=5)
        self.employee_combobox = ttk.Combobox(self, values=[])
        self.employee_combobox.grid(row=8, column=1, padx=5, pady=5)

        # Кнопка сохранения
        self.save_button = ttk.Button(self, text="Сохранить", command=self.save_changes)
        self.save_button.grid(row=9, column=1, padx=5, pady=5)

    def load_departments_and_employees(self):
        """Загружает списки отделов и сотрудников из базы данных."""
        try:
            self.departments = self.db_connector.fetch_all_departments()
            self.employees = self.db_connector.fetch_all_employees()

            # Обновляем значения combobox'ов
            self.department_combobox['values'] = [d.name for d in self.departments]
            self.employee_combobox['values'] = [e.name for e in self.employees]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке отделов и сотрудников: {e}")

    def populate_fields(self):
        """Заполняет поля данными об устройстве, включая отдел и сотрудника."""
        self.name_entry.insert(0, self.device.name)
        self.category_entry.insert(0, self.device.category)
        self.serial_number_entry.insert(0, self.device.serial_number)
        self.status_entry.insert(0, self.device.status)
        self.purchase_date_entry.insert(0, str(self.device.purchase_date))
        self.warranty_until_entry.insert(0, str(self.device.warranty_until))
        self.description_entry.insert(0, self.device.description)

        # Выбираем отдел и сотрудника в combobox'ах
        if self.device.department_id:
            department = next((d for d in self.departments if d.id == self.device.department_id), None)
            if department:
                self.department_combobox.set(department.name)
        if self.device.employee_id:
            employee = next((e for e in self.employees if e.id == self.device.employee_id), None)
            if employee:
                self.employee_combobox.set(employee.name)

    def save_changes(self):
        """Сохраняет изменения в базе данных."""
        try:
            name = self.name_entry.get()
            category = self.category_entry.get()
            serial_number = self.serial_number_entry.get()
            status = self.status_entry.get()
            purchase_date_str = self.purchase_date_entry.get()
            warranty_until_str = self.warranty_until_entry.get()
            description = self.description_entry.get()

            # Получаем выбранные отдел и сотрудника
            selected_department_name = self.department_combobox.get()
            selected_employee_name = self.employee_combobox.get()

            # Находим соответствующие объекты Department и Employee
            department = next((d for d in self.departments if d.name == selected_department_name), None)
            employee = next((e for e in self.employees if e.name == selected_employee_name), None)

            # Проверяем, что отдел и сотрудник были выбраны
            if not department:
                messagebox.showerror("Ошибка", "Выберите отдел.")
                return
            if not employee:
                messagebox.showerror("Ошибка", "Выберите ответственного сотрудника.")
                return

            # Преобразуем строки в даты
            purchase_date = datetime.datetime.strptime(purchase_date_str, "%Y-%m-%d").date()
            warranty_until = datetime.datetime.strptime(warranty_until_str, "%Y-%m-%d").date()

            # Обновляем данные устройства
            self.device.name = name
            self.device.category = category
            self.device.serial_number = serial_number
            self.device.status = status
            self.device.purchase_date = purchase_date
            self.device.warranty_until = warranty_until
            self.device.description = description
            self.device.department_id = department.id
            self.device.employee_id = employee.id

            self.db_connector.update_device(self.device)
            messagebox.showinfo("Успех", "Изменения успешно сохранены!")
            self.refresh_callback()  # Обновляем таблицу в главном окне
            self.destroy()  # Закрываем окно редактирования
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты (YYYY-MM-DD)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении изменений: {e}")