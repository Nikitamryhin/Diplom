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
        self.employees = []
        self.departments = []
        self.selected_department_id = None
        self.create_widgets()
        self.load_departments()
        self.load_devices()

    def create_widgets(self):
        # Фрейм для кнопок отделов
        self.department_frame = tk.Frame(self.root)
        self.department_frame.pack(pady=5)

        # Кнопки управления устройствами
        self.add_button = ttk.Button(self.root, text="Добавить устройство", command=self.open_add_device_window)
        self.add_button.pack(pady=5)

        self.edit_button = ttk.Button(self.root, text="Редактировать устройство", command=self.open_edit_device_window)
        self.edit_button.pack(pady=5)

        self.delete_button = ttk.Button(self.root, text="Удалить устройство", command=self.delete_device)
        self.delete_button.pack(pady=5)

        # Кнопки управления отделами и сотрудниками
        self.add_department_button = ttk.Button(self.root, text="Добавить отдел", command=self.open_add_department_window)
        self.add_department_button.pack(pady=5)

        self.add_employee_button = ttk.Button(self.root, text="Добавить сотрудника", command=self.open_add_employee_window)
        self.add_employee_button.pack(pady=5)

        # Таблица для отображения устройств
        self.device_tree = ttk.Treeview(self.root, columns=("ID", "Название", "Категория", "Серийный номер", "Статус"), show="headings")
        self.device_tree.heading("ID", text="ID")
        self.device_tree.heading("Название", text="Название")
        self.device_tree.heading("Категория", text="Категория")
        self.device_tree.heading("Серийный номер", text="Серийный номер")
        self.device_tree.heading("Статус", text="Статус")
        self.device_tree.pack(expand=True, fill=tk.BOTH)

        # Таблица для отображения сотрудников
        self.employee_tree = ttk.Treeview(self.root, columns=("ID", "Имя", "Должность"), show="headings")
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Имя", text="Имя")
        self.employee_tree.heading("Должность", text="Должность")
        self.employee_tree.pack(expand=True, fill=tk.BOTH)

    def load_departments(self):
        """Загружает список отделов из базы данных и создает кнопки для каждого отдела."""
        # Очищаем фрейм с кнопками отделов
        for widget in self.department_frame.winfo_children():
            widget.destroy()

        # Загружаем отделы из базы данных
        self.departments = self.db_connector.fetch_all_departments()

        # Создаем кнопку для каждого отдела
        for department in self.departments:
            button = ttk.Button(self.department_frame, text=department.name, command=lambda dep_id=department.id: self.load_department_data(dep_id))
            button.pack(side=tk.LEFT, padx=5)

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
        print(f"Error loading departments: {e}")  # Выводим ошибку в консоль
        tk.messagebox.showerror("Ошибка", f"Ошибка при загрузке отделов: {e}")

def load_devices(self, department_id=None):
        """Загружает данные об устройствах из базы данных и отображает их в таблице."""
        try:
            # Очищаем таблицу устройств
            for item in self.device_tree.get_children():
                self.device_tree.delete(item)

            # Загружаем устройства из базы данных
            if department_id is None:
                devices = self.db_connector.fetch_all_devices()
            else:
                devices = [d for d in self.db_connector.fetch_all_devices() if d.department_id == department_id]

            for device in devices:
                self.device_tree.insert("", tk.END, values=(device.id, device.name, device.category, device.serial_number, device.status))
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при загрузке устройств: {e}")

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
            employees = self.db_connector.fetch_employees_by_department(department_id)  # Используем новый метод

        for employee in employees:
            self.employee_tree.insert("", tk.END, values=(employee.id, employee.name, employee.position))
    except Exception as e:
        print(f"Error loading employees: {e}")  # Выводим ошибку в консоль
        tk.messagebox.showerror("Ошибка", f"Ошибка при загрузке сотрудников: {e}")

def open_add_device_window(self):
        """Открывает окно для добавления нового устройства."""
        add_device_window = AddDeviceWindow(self.root, self.db_connector, self.load_devices) # Передаем функцию load_devices

def open_edit_device_window(self):
        selected_item = self.device_tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите устройство для редактирования.")
            return

        device_id = self.device_tree.item(selected_item[0])['values'][0]

        try:
            devices = self.db_connector.fetch_all_devices()
            device = next((d for d in devices if d.id == device_id), None)

            if device:
                edit_window = EditDeviceWindow(self.root, self.db_connector, device, self.load_devices)
            else:
                tk.messagebox.showerror("Ошибка", "Устройство не найдено.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при открытии окна редактирования: {e}")

def delete_device(self):
        selected_item = self.device_tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите устройство для удаления.")
            return

        device_id = self.device_tree.item(selected_item[0])['values'][0]

        try:
            device = next((d for d in self.db_connector.fetch_all_devices() if d.id == device_id), None)

            if device is None:
                tk.messagebox.showerror("Ошибка", "Устройство не найдено в базе данных.")
                return

            if tk.messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить устройство '{device.name}'?"):
                self.db_connector.delete_device(device_id)
                self.load_devices()
                tk.messagebox.showinfo("Успех", "Устройство успешно удалено.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при удалении устройства: {e}")

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
            self.db_connector.delete_department(department_id) # Удаляем отдел из базы данных
            self.load_departments() # Обновляем Treeview с отделами
            tk.messagebox.showinfo("Успех", "Отдел успешно удален.")
    except Exception as e:
        tk.messagebox.showerror("Ошибка", f"Ошибка при удалении отдела: {e}")

def open_add_department_window(self):
        """Открывает окно для добавления нового отдела."""
        add_department_window = AddDepartmentWindow(self.root, self.db_connector, self.load_departments)

def open_add_employee_window(self):
        """Открывает окно для добавления нового сотрудника."""
        add_employee_window = AddEmployeeWindow(self.root, self.db_connector, self.load_employees)