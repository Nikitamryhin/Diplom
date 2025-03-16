import tkinter as tk
from tkinter import ttk, messagebox
from gui.add_device_window import AddDeviceWindow
from gui.edit_device_window import EditDeviceWindow
from gui.add_department_window import AddDepartmentWindow
from gui.add_employee_window import AddEmployeeWindow
from models.device import Device

class MainWindow:
    def __init__(self, root, db_connector):
        self.root = root
        self.root.title("Управление устройствами")
        self.db_connector = db_connector
        self.devices = []
        self.create_widgets()
        self.load_devices()
        self.load_departments()
        self.load_employees()

    def create_widgets(self):
        # Кнопки управления устройствами
        self.add_device_button = ttk.Button(self.root, text="Добавить устройство", command=self.open_add_device_window)
        self.add_device_button.pack(pady=5)

        self.edit_device_button = ttk.Button(self.root, text="Редактировать устройство", command=self.open_edit_device_window)
        self.edit_device_button.pack(pady=5)

        self.delete_device_button = ttk.Button(self.root, text="Удалить устройство", command=self.delete_device)
        self.delete_device_button.pack(pady=5)

        # Кнопки управления отделами
        self.add_department_button = ttk.Button(self.root, text="Добавить отдел", command=self.open_add_department_window)
        self.add_department_button.pack(pady=5)

        self.edit_department_button = ttk.Button(self.root, text="Редактировать отдел", command=self.open_edit_department_window)  # TODO: Implement edit department window
        self.edit_department_button.pack(pady=5)

        self.delete_department_button = ttk.Button(self.root, text="Удалить отдел", command=self.delete_department)
        self.delete_department_button.pack(pady=5)

        # Кнопки управления сотрудниками
        self.add_employee_button = ttk.Button(self.root, text="Добавить сотрудника", command=self.open_add_employee_window)
        self.add_employee_button.pack(pady=5)

        # Treeview для устройств
        self.tree = ttk.Treeview(self.root, columns=("ID", "Название", "Категория", "Серийный номер", "Статус", "Отдел", "Ответственный"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Серийный номер", text="Серийный номер")
        self.tree.heading("Статус", text="Статус")
        self.tree.heading("Отдел", text="Отдел")
        self.tree.heading("Ответственный", text="Ответственный")
        self.tree.pack(expand=True, fill=tk.BOTH)

        # Treeview для отделов
        self.department_tree = ttk.Treeview(self.root, columns=("ID", "Название"), show="headings")
        self.department_tree.heading("ID", text="ID")
        self.department_tree.heading("Название", text="Название")
        self.department_tree.pack(expand=True, fill=tk.BOTH)

        # Treeview для сотрудников
        self.employee_tree = ttk.Treeview(self.root, columns=("ID", "Имя", "Должность"), show="headings")
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Имя", text="Имя")
        self.employee_tree.heading("Должность", text="Должность")
        self.employee_tree.pack(expand=True, fill=tk.BOTH)

    def load_devices(self):
        """Загружает список устройств в Treeview."""
        try:
            # Очищаем Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            devices = self.db_connector.fetch_all_devices()
            for device in devices:
                self.tree.insert("", tk.END, values=(device.id, device.name, device.category, device.serial_number, device.status, device.department_id, device.employee_id))
        except Exception as e:
            print(f"Error loading devices: {e}")
            tk.messagebox.showerror("Ошибка", f"Ошибка при загрузке устройств: {e}")

    def delete_device(self):
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите устройство для удаления.")
            return

        device_id = self.tree.item(selected_item[0])['values'][0]
        device_name = self.tree.item(selected_item[0])['values'][1]

        if tk.messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить устройство '{device_name}'?"):
            try:
                self.db_connector.delete_device(device_id)
                self.load_devices()
                tk.messagebox.showinfo("Успех", "Устройство успешно удалено.")
            except Exception as e:
                tk.messagebox.showerror("Ошибка", f"Ошибка при удалении устройства: {e}")

    def open_edit_device_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите устройство для редактирования.")
            return

        device_id = self.tree.item(selected_item[0])['values'][0]

        try:
            # Получаем устройство из базы данных по ID
            devices = self.db_connector.fetch_all_devices()
            device = next((d for d in devices if d.id == device_id), None)

            if device:
                edit_window = EditDeviceWindow(self.root, self.db_connector, device, self.load_devices)
            else:
                tk.messagebox.showerror("Ошибка", "Устройство не найдено.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при открытии окна редактирования: {e}")

    def open_add_device_window(self):
        """Открывает окно для добавления нового устройства."""
        add_device_window = AddDeviceWindow(self.root, self.db_connector, self.load_devices)

    def load_departments(self):
        """Загружает список отделов в Treeview."""
        try:
            # Очищаем Treeview
            for item in self.department_tree.get_children():
                self.department_tree.delete(item)

            departments = self.db_connector.fetch_all_departments()
            for department in departments:
                self.department_tree.insert("", tk.END, values=(department.id, department.name))
        except Exception as e:
            print(f"Error loading departments: {e}")
            tk.messagebox.showerror("Ошибка", f"Ошибка при загрузке отделов: {e}")

    def delete_department(self):
        selected_item = self.department_tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите отдел для удаления.")
            return

        department_id = self.department_tree.item(selected_item[0])['values'][0]
        department_name = self.department_tree.item(selected_item[0])['values'][1]

        try:
            # Проверяем, есть ли устройства, связанные с этим отделом
            has_devices = self.db_connector.check_if_department_has_devices(department_id)
            if has_devices:
                tk.messagebox.showerror("Ошибка", "Невозможно удалить отдел. Сначала удалите или переместите устройства, связанные с этим отделом.")
                return  # Прерываем удаление

            if tk.messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить отдел '{department_name}'?"):
                self.db_connector.delete_department(department_id)
                self.load_departments()
                tk.messagebox.showinfo("Успех", "Отдел успешно удален.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при удалении отдела: {e}")

    def open_add_department_window(self):
        """Открывает окно для добавления нового отдела."""
        add_department_window = AddDepartmentWindow(self.root, self.db_connector, self.load_departments)

    def open_edit_department_window(self):
        """Открывает окно для редактирования отдела."""
        pass #TODO

    def open_add_employee_window(self):
        add_employee_window = AddEmployeeWindow(self.root, self.db_connector, self.load_employees)

    def load_employees(self, department_id=None):
        """Загружает данные о сотрудниках из базы данных и отображает их в таблице."""
        try:
            # Очищаем таблицу сотрудников
            for item in self.employee_tree.get_children():
                self.employee_tree.delete(item)

            # Загружаем сотрудников из базы данных
            if department_id is None:
                employees = self.db_connector.fetch_all_employees()
            else:
                employees = self.db_connector.fetch_employees_by_department(department_id)

            for employee in employees:
                self.employee_tree.insert("", tk.END, values=(employee.id, employee.name, employee.position))
        except Exception as e:
            print(f"Error loading employees: {e}")
            tk.messagebox.showerror("Ошибка", f"Ошибка при загрузке сотрудников: {e}")