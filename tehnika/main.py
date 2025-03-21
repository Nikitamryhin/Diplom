import tkinter as tk
from tkinter import ttk, messagebox
import db.database as database
import sqlite3


# --- Класс AddDepartmentWindow ---
class AddDepartmentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Добавить отдел")
        self.geometry("300x150")

        self.name_label = ttk.Label(self, text="Название отдела:")
        self.name_label.pack(pady=5)

        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_department)
        self.add_button.pack(pady=10)

    def add_department(self):
        name = self.name_entry.get()
        if name:
            database.add_department(name)
            self.parent.load_departments()
            self.destroy()
        else:
            messagebox.showinfo("Внимание", "Введите название отдела.")


# --- Класс EditDepartmentWindow ---
class EditDepartmentWindow(tk.Toplevel):
    def __init__(self, parent, department_id):
        super().__init__(parent)
        self.parent = parent
        self.department_id = department_id
        self.title("Редактировать отдел")
        self.geometry("300x150")

        department = database.get_department(department_id)

        self.name_label = ttk.Label(self, text="Название отдела:")
        self.name_label.pack(pady=5)

        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, department[1])

        self.save_button = ttk.Button(self, text="Сохранить", command=self.save_department)
        self.save_button.pack(pady=10)

    def save_department(self):
        name = self.name_entry.get()
        if name:
            database.update_department(self.department_id, name)
            self.parent.load_departments()
            self.destroy()
        else:
            messagebox.showinfo("Внимание", "Введите название отдела.")


# --- Класс AddDeviceWindow ---
class AddDeviceWindow(tk.Toplevel):
    def __init__(self, parent, department_id):
        super().__init__(parent)
        self.parent = parent
        self.department_id = department_id
        self.title("Добавить устройство")
        self.geometry("400x400")

        self.type_label = ttk.Label(self, text="Тип:")
        self.type_label.pack(pady=2)
        self.type_entry = ttk.Entry(self)
        self.type_entry.pack(pady=2)

        self.model_label = ttk.Label(self, text="Модель:")
        self.model_label.pack(pady=2)
        self.model_entry = ttk.Entry(self)
        self.model_entry.pack(pady=2)

        self.serial_number_label = ttk.Label(self, text="Серийный номер:")
        self.serial_number_label.pack(pady=2)
        self.serial_number_entry = ttk.Entry(self)
        self.serial_number_entry.pack(pady=2)

        self.inventory_number_label = ttk.Label(self, text="Инвентарный номер:")
        self.inventory_number_label.pack(pady=2)
        self.inventory_number_entry = ttk.Entry(self)
        self.inventory_number_entry.pack(pady=2)

        self.cpu_label = ttk.Label(self, text="CPU:")
        self.cpu_label.pack(pady=2)
        self.cpu_entry = ttk.Entry(self)
        self.cpu_entry.pack(pady=2)

        self.memory_label = ttk.Label(self, text="Memory:")
        self.memory_label.pack(pady=2)
        self.memory_entry = ttk.Entry(self)
        self.memory_entry.pack(pady=2)

        self.hdd_label = ttk.Label(self, text="HDD:")
        self.hdd_label.pack(pady=2)
        self.hdd_entry = ttk.Entry(self)
        self.hdd_entry.pack(pady=2)

        self.gpu_label = ttk.Label(self, text="GPU:")
        self.gpu_label.pack(pady=2)
        self.gpu_entry = ttk.Entry(self)
        self.gpu_entry.pack(pady=2)

        self.status_label = ttk.Label(self, text="Статус:")
        self.status_label.pack(pady=2)
        self.status_entry = ttk.Entry(self)
        self.status_entry.pack(pady=2)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_device)
        self.add_button.pack(pady=10)

    def add_device(self):
        device_data = {
            "department_id": self.department_id,
            "type": self.type_entry.get(),
            "model": self.model_entry.get(),
            "serial_number": self.serial_number_entry.get(),
            "inventory_number": self.inventory_number_entry.get(),
            "cpu": self.cpu_entry.get(),
            "memory": self.memory_entry.get(),
            "hdd": self.hdd_entry.get(),
            "gpu": self.gpu_entry.get(),
            "status": self.status_entry.get()
        }

        if all(device_data.values()):
            database.add_device(device_data)
            self.parent.load_devices()
            self.destroy()
        else:
            messagebox.showinfo("Внимание", "Заполните все поля.")


# --- Класс EditDeviceWindow ---
class EditDeviceWindow(tk.Toplevel):
    def __init__(self, parent, device_id):
        super().__init__(parent)
        self.parent = parent
        self.device_id = device_id
        self.title("Редактировать устройство")
        self.geometry("400x400")

        device = database.get_device(device_id)

        self.type_label = ttk.Label(self, text="Тип:")
        self.type_label.pack(pady=2)
        self.type_entry = ttk.Entry(self)
        self.type_entry.pack(pady=2)
        self.type_entry.insert(0, device[2])

        self.model_label = ttk.Label(self, text="Модель:")
        self.model_label.pack(pady=2)
        self.model_entry = ttk.Entry(self)
        self.model_entry.pack(pady=2)
        self.model_entry.insert(0, device[3])

        self.serial_number_label = ttk.Label(self, text="Серийный номер:")
        self.serial_number_label.pack(pady=2)
        self.serial_number_entry = ttk.Entry(self)
        self.serial_number_entry.pack(pady=2)
        self.serial_number_entry.insert(0, device[4])

        self.inventory_number_label = ttk.Label(self, text="Инвентарный номер:")
        self.inventory_number_label.pack(pady=2)
        self.inventory_number_entry = ttk.Entry(self)
        self.inventory_number_entry.pack(pady=2)
        self.inventory_number_entry.insert(0, device[5])

        self.cpu_label = ttk.Label(self, text="CPU:")
        self.cpu_label.pack(pady=2)
        self.cpu_entry = ttk.Entry(self)
        self.cpu_entry.pack(pady=2)
        self.cpu_entry.insert(0, device[6])

        self.memory_label = ttk.Label(self, text="Memory:")
        self.memory_label.pack(pady=2)
        self.memory_entry = ttk.Entry(self)
        self.memory_entry.pack(pady=2)
        self.memory_entry.insert(0, device[7])

        self.hdd_label = ttk.Label(self, text="HDD:")
        self.hdd_label.pack(pady=2)
        self.hdd_entry = ttk.Entry(self)
        self.hdd_entry.pack(pady=2)
        self.hdd_entry.insert(0, device[8])

        self.gpu_label = ttk.Label(self, text="GPU:")
        self.gpu_label.pack(pady=2)
        self.gpu_entry = ttk.Entry(self)
        self.gpu_entry.pack(pady=2)
        self.gpu_entry.insert(0, device[9])

        self.status_label = ttk.Label(self, text="Статус:")
        self.status_label.pack(pady=2)
        self.status_entry = ttk.Entry(self)
        self.status_entry.pack(pady=2)
        self.status_entry.insert(0, device[10])

        self.save_button = ttk.Button(self, text="Сохранить", command=self.save_device)
        self.save_button.pack(pady=10)

    def save_device(self):
        device_data = {
            "id": self.device_id,
            "type": self.type_entry.get(),
            "model": self.model_entry.get(),
            "serial_number": self.serial_number_entry.get(),
            "inventory_number": self.inventory_number_entry.get(),
            "cpu": self.cpu_entry.get(),
            "memory": self.memory_entry.get(),
            "hdd": self.hdd_entry.get(),
            "gpu": self.gpu_entry.get(),
            "status": self.status_entry.get()
        }

        if all(device_data.values()):
            database.update_device(device_data)
            self.parent.load_devices()
            self.destroy()
        else:
            messagebox.showinfo("Внимание", "Заполните все поля.")


# --- Класс PeripheralsWindow ---
class PeripheralsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Управление периферией")
        self.geometry("600x400")

        self.peripherals_tree = ttk.Treeview(self, columns=("id", "name", "type", "interface", "manufacturer", "resolution", "print_type", "print_speed", "quantity", "price", "description"), show="headings")
        self.peripherals_tree.heading("id", text="ID")
        self.peripherals_tree.heading("name", text="Название")
        self.peripherals_tree.heading("type", text="Тип")
        self.peripherals_tree.heading("interface", text="Интерфейс")
        self.peripherals_tree.heading("manufacturer", text="Производитель")
        self.peripherals_tree.heading("resolution", text="Разрешение")
        self.peripherals_tree.heading("print_type", text="Тип печати")
        self.peripherals_tree.heading("print_speed", text="Скорость печати")
        self.peripherals_tree.heading("quantity", text="Количество")
        self.peripherals_tree.heading("price", text="Цена")
        self.peripherals_tree.heading("description", text="Описание")

        self.peripherals_tree.column("id", width=30)
        self.peripherals_tree.column("name", width=100)
        self.peripherals_tree.column("type", width=80)
        self.peripherals_tree.column("interface", width=80)
        self.peripherals_tree.column("manufacturer", width=100)
        self.peripherals_tree.column("resolution", width=80)
        self.peripherals_tree.column("print_type", width=80)
        self.peripherals_tree.column("print_speed", width=80)
        self.peripherals_tree.column("quantity", width=50)
        self.peripherals_tree.column("price", width=50)
        self.peripherals_tree.column("description", width=150)
        self.peripherals_tree.pack(fill="both", expand=True)
        self.peripherals_tree.bind("<ButtonRelease-1>", self.select_peripheral)

        self.load_peripherals()

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(pady=5)

        self.add_button = ttk.Button(self.buttons_frame, text="Добавить", command=self.open_add_peripheral_window)
        self.add_button.pack(side=tk.LEFT, padx=2)

        self.edit_button = ttk.Button(self.buttons_frame, text="Редактировать", command=self.open_edit_peripheral_window)
        self.edit_button.pack(side=tk.LEFT, padx=2)

        self.delete_button = ttk.Button(self.buttons_frame, text="Удалить", command=self.delete_peripheral)
        self.delete_button.pack(side=tk.LEFT, padx=2)

        self.selected_peripheral_id = None

    def load_peripherals(self):
        """Загружает список периферии в Treeview"""
        for item in self.peripherals_tree.get_children():
            self.peripherals_tree.delete(item)

        peripherals = database.get_peripherals()
        for peripheral in peripherals:
            self.peripherals_tree.insert("", tk.END, values=(
                peripheral[0], peripheral[1], peripheral[2], peripheral[3], peripheral[4], peripheral[5], peripheral[6], peripheral[7], peripheral[8], peripheral[9], peripheral[10]))

    def open_add_peripheral_window(self):
        """Открывает окно для добавления периферии"""
        AddPeripheralWindow(self)

    def open_edit_peripheral_window(self):
        """Открывает окно для редактирования периферии"""
        if self.selected_peripheral_id:
            EditPeripheralWindow(self, self.selected_peripheral_id)
        else:
            messagebox.showinfo("Внимание", "Выберите периферию для редактирования.")

    def delete_peripheral(self):
        """Удаляет выбранную периферию"""
        if self.selected_peripheral_id:
            if messagebox.askyesno("Удаление периферии", "Вы уверены, что хотите удалить эту периферию?", parent=self):
                database.delete_peripheral(self.selected_peripheral_id)
                self.load_peripherals()
        else:
            messagebox.showinfo("Внимание", "Выберите периферию для удаления.")

    def select_peripheral(self, event):
        """Вызывается при выборе периферии в Treeview"""
        selected_item = self.peripherals_tree.selection()[0]
        self.selected_peripheral_id = self.peripherals_tree.item(selected_item, 'values')[0]


# --- Класс AddPeripheralWindow ---
class AddPeripheralWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Добавить периферию")
        self.geometry("400x500")

        self.name_label = ttk.Label(self, text="Название:")
        self.name_label.pack(pady=2)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=2)

        self.type_label = ttk.Label(self, text="Тип:")
        self.type_label.pack(pady=2)
        self.type_entry = ttk.Entry(self)
        self.type_entry.pack(pady=2)

        self.interface_label = ttk.Label(self, text="Интерфейс:")
        self.interface_label.pack(pady=2)
        self.interface_entry = ttk.Entry(self)
        self.interface_entry.pack(pady=2)

        self.manufacturer_label = ttk.Label(self, text="Производитель:")
        self.manufacturer_label.pack(pady=2)
        self.manufacturer_entry = ttk.Entry(self)
        self.manufacturer_entry.pack(pady=2)

        self.resolution_label = ttk.Label(self, text="Разрешение:")
        self.resolution_label.pack(pady=2)
        self.resolution_entry = ttk.Entry(self)
        self.resolution_entry.pack(pady=2)

        self.print_type_label = ttk.Label(self, text="Тип печати:")
        self.print_type_label.pack(pady=2)
        self.print_type_entry = ttk.Entry(self)
        self.print_type_entry.pack(pady=2)

        self.print_speed_label = ttk.Label(self, text="Скорость печати:")
        self.print_speed_label.pack(pady=2)
        self.print_speed_entry = ttk.Entry(self)
        self.print_speed_entry.pack(pady=2)

        self.quantity_label = ttk.Label(self, text="Количество:")
        self.quantity_label.pack(pady=2)
        self.quantity_entry = ttk.Entry(self)
        self.quantity_entry.pack(pady=2)

        self.price_label = ttk.Label(self, text="Цена:")
        self.price_label.pack(pady=2)
        self.price_entry = ttk.Entry(self)
        self.price_entry.pack(pady=2)

        self.description_label = ttk.Label(self, text="Описание:")
        self.description_label.pack(pady=2)
        self.description_entry = ttk.Entry(self)
        self.description_entry.pack(pady=2)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_peripheral)
        self.add_button.pack(pady=10)

    def add_peripheral(self):
        peripheral_data = {
            "name": self.name_entry.get(),
            "type": self.type_entry.get(),
            "interface": self.interface_entry.get(),
            "manufacturer": self.manufacturer_entry.get(),
            "resolution": self.resolution_entry.get(),
            "print_type": self.print_type_entry.get(),
            "print_speed": self.print_speed_entry.get(),
            "quantity": self.quantity_entry.get(),
            "price": self.price_entry.get(),
            "description": self.description_entry.get()
        }

        if all(peripheral_data.values()):
            database.add_peripheral(peripheral_data)
            self.parent.load_peripherals()
            self.destroy()
        else:
            messagebox.showinfo("Внимание", "Заполните все поля.")


# --- Класс EditPeripheralWindow ---
class EditPeripheralWindow(tk.Toplevel):
    def __init__(self, parent, peripheral_id):
        super().__init__(parent)
        self.parent = parent
        self.peripheral_id = peripheral_id
        self.title("Редактировать периферию")
        self.geometry("400x500")

        peripheral = database.get_peripheral(peripheral_id)

        self.name_label = ttk.Label(self, text="Название:")
        self.name_label.pack(pady=2)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=2)
        self.name_entry.insert(0, peripheral[1])

        self.type_label = ttk.Label(self, text="Тип:")
        self.type_label.pack(pady=2)
        self.type_entry = ttk.Entry(self)
        self.type_entry.pack(pady=2)
        self.type_entry.insert(0, peripheral[2])

        self.interface_label = ttk.Label(self, text="Интерфейс:")
        self.interface_label.pack(pady=2)
        self.interface_entry = ttk.Entry(self)
        self.interface_entry.pack(pady=2)
        self.interface_entry.insert(0, peripheral[3])

        self.manufacturer_label = ttk.Label(self, text="Производитель:")
        self.manufacturer_label.pack(pady=2)
        self.manufacturer_entry = ttk.Entry(self)
        self.manufacturer_entry.pack(pady=2)
        self.manufacturer_entry.insert(0, peripheral[4])

        self.resolution_label = ttk.Label(self, text="Разрешение:")
        self.resolution_label.pack(pady=2)
        self.resolution_entry = ttk.Entry(self)
        self.resolution_entry.pack(pady=2)
        self.resolution_entry.insert(0, peripheral[5])

        self.print_type_label = ttk.Label(self, text="Тип печати:")
        self.print_type_label.pack(pady=2)
        self.print_type_entry = ttk.Entry(self)
        self.print_type_entry.pack(pady=2)
        self.print_type_entry.insert(0, peripheral[6])

        self.print_speed_label = ttk.Label(self, text="Скорость печати:")
        self.print_speed_label.pack(pady=2)
        self.print_speed_entry = ttk.Entry(self)
        self.print_speed_entry.pack(pady=2)
        self.print_speed_entry.insert(0, peripheral[7])

        self.quantity_label = ttk.Label(self, text="Количество:")
        self.quantity_label.pack(pady=2)
        self.quantity_entry = ttk.Entry(self)
        self.quantity_entry.pack(pady=2)
        self.quantity_entry.insert(0, peripheral[8])

        self.price_label = ttk.Label(self, text="Цена:")
        self.price_label.pack(pady=2)
        self.price_entry = ttk.Entry(self)
        self.price_entry.pack(pady=2)
        self.price_entry.insert(0, peripheral[9])

        self.description_label = ttk.Label(self, text="Описание:")
        self.description_label.pack(pady=2)
        self.description_entry = ttk.Entry(self)
        self.description_entry.pack(pady=2)
        self.description_entry.insert(0, peripheral[10])

        self.save_button = ttk.Button(self, text="Сохранить", command=self.save_peripheral)
        self.save_button.pack(pady=10)

    def save_peripheral(self):
        peripheral_data = {
            "id": self.peripheral_id,
            "name": self.name_entry.get(),
            "type": self.type_entry.get(),
            "interface": self.interface_entry.get(),
            "manufacturer": self.manufacturer_entry.get(),
            "resolution": self.resolution_entry.get(),
            "print_type": self.print_type_entry.get(),
            "print_speed": self.print_speed_entry.get(),
            "quantity": self.quantity_entry.get(),
            "price": self.price_entry.get(),
            "description": self.description_entry.get()
        }

        if all(peripheral_data.values()):
            database.update_peripheral(peripheral_data)
            self.parent.load_peripherals()
            self.destroy()
        else:
            messagebox.showinfo("Внимание", "Заполните все поля.")


# --- Класс AddDevicePeripheralWindow ---
class AddDevicePeripheralWindow(tk.Toplevel):
    def __init__(self, parent, device_id):
        super().__init__(parent)
        self.parent = parent
        self.device_id = device_id
        self.title("Добавить периферию к устройству")
        self.geometry("300x200")

        self.peripheral_label = ttk.Label(self, text="Выберите периферию:")
        self.peripheral_label.pack(pady=5)

        self.peripheral_combobox = ttk.Combobox(self, values=self.get_peripheral_names())
        self.peripheral_combobox.pack(pady=5)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_device_peripheral)
        self.add_button.pack(pady=10)

    def get_peripheral_names(self):
        """Получает список названий периферии из базы данных"""
        peripherals = database.get_peripherals()
        return [peripheral[1] for peripheral in peripherals]  # Возвращаем только названия

    def add_device_peripheral(self):
        """Добавляет выбранную периферию к устройству"""
        peripheral_name = self.peripheral_combobox.get()
        if peripheral_name:
            peripheral = database.get_peripheral_by_name(peripheral_name)
            if peripheral:
                database.add_device_peripheral(self.device_id, peripheral[0])
                self.parent.load_device_peripherals()
                self.destroy()
            else:
                messagebox.showerror("Ошибка", "Периферийное устройство не найдено.")
        else:
            messagebox.showinfo("Внимание", "Выберите периферию.")


# --- Класс MainWindow ---
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Учет и контроль состояния компьютерной техники")
        self.geometry("1200x800")

        # ---  Главное меню ---
        self.main_menu = tk.Menu(self)
        self.config(menu=self.main_menu)

        # ---  Меню Файл ---
        filemenu = tk.Menu(self.main_menu, tearoff=0)
        filemenu.add_command(label="Управление устройствами",
                             command=self.open_peripherals_window)  # Добавляем пункт в меню
        filemenu.add_command(label="Сформировать отчет", command=self.generate_report)  # Добавлена команда для отчета
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.quit)
        self.main_menu.add_cascade(label="Файл", menu=filemenu)

        # ---  Фреймы ---
        self.departments_frame = ttk.Frame(self)
        self.departments_frame.pack(side=tk.LEFT, fill="y", padx=5, pady=5)

        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5, pady=5)

        self.devices_frame = ttk.Frame(self)
        self.devices_frame.pack(side=tk.TOP, fill="both", expand=True, padx=5, pady=5)

        # --- Отделы ---
        self.departments_label = ttk.Label(self.departments_frame, text="Отделы:")
        self.departments_label.pack(pady=2)

        self.departments_tree = ttk.Treeview(self.departments_frame, columns=("id", "name"), show="headings")
        self.departments_tree.heading("id", text="ID")
        self.departments_tree.heading("name", text="Название")
        self.departments_tree.column("id", width=30)
        self.departments_tree.column("name", width=200)
        self.departments_tree.pack(fill="y", expand=True)
        self.departments_tree.bind("<ButtonRelease-1>", self.select_department)  # При клике вызываем функцию

        self.load_departments()

        # --- Кнопки управления отделами ---
        self.departments_buttons_frame = ttk.Frame(self.departments_frame)
        self.departments_buttons_frame.pack(pady=5)

        self.add_department_button = ttk.Button(self.departments_buttons_frame, text="Добавить",
                                                 command=self.open_add_department_window)
        self.add_department_button.pack(side=tk.LEFT, padx=2)

        self.edit_department_button = ttk.Button(self.departments_buttons_frame, text="Редактировать",
                                                  command=self.open_edit_department_window)
        self.edit_department_button.pack(side=tk.LEFT, padx=2)

        self.delete_department_button = ttk.Button(self.departments_buttons_frame, text="Удалить",
                                                    command=self.delete_department)
        self.delete_department_button.pack(side=tk.LEFT, padx=2)

        # ---  Информация об отделе ---
        self.department_info_label = ttk.Label(self.info_frame, text="Информация об отделе:")
        self.department_info_label.pack(pady=2)

        self.department_name_label = ttk.Label(self.info_frame, text="Название отдела:")
        self.department_name_label.pack(pady=2)

        # ---  Компьютерная техника ---
        self.devices_label = ttk.Label(self.devices_frame, text="Компьютерная техника в отделе:")
        self.devices_label.pack(pady=2)

        self.devices_tree = ttk.Treeview(self.devices_frame, columns=(
            "id", "type", "model", "serial_number", "inventory_number", "cpu", "memory", "hdd", "gpu", "status"),
                                              show="headings")
        self.devices_tree.heading("id", text="ID")
        self.devices_tree.heading("type", text="Тип")
        self.devices_tree.heading("model", text="Модель")
        self.devices_tree.heading("serial_number", text="Серийный номер")
        self.devices_tree.heading("inventory_number", text="Инв. номер")
        self.devices_tree.heading("cpu", text="CPU")
        self.devices_tree.heading("memory", text="Memory")
        self.devices_tree.heading("hdd", text="HDD")
        self.devices_tree.heading("gpu", text="GPU")
        self.devices_tree.heading("status", text="Статус")

        self.devices_tree.column("id", width=30)
        self.devices_tree.column("type", width=80)
        self.devices_tree.column("model", width=100)
        self.devices_tree.column("serial_number", width=100)
        self.devices_tree.column("inventory_number", width=100)
        self.devices_tree.column("cpu", width=80)
        self.devices_tree.column("memory", width=80)
        self.devices_tree.column("hdd", width=80)
        self.devices_tree.column("gpu", width=80)
        self.devices_tree.column("status", width=80)
        self.devices_tree.pack(fill="both", expand=True)
        self.devices_tree.bind("<ButtonRelease-1>", self.select_device)  # При клике вызываем функцию

        # --- Кнопки управления устройствами ---
        self.devices_buttons_frame = ttk.Frame(self.devices_frame)
        self.devices_buttons_frame.pack(pady=5)

        self.add_device_button = ttk.Button(self.devices_buttons_frame, text="Добавить",
                                             command=self.open_add_device_window)
        self.add_device_button.pack(side=tk.LEFT, padx=2)

        self.edit_device_button = ttk.Button(self.devices_buttons_frame, text="Редактировать",
                                              command=self.open_edit_device_window)
        self.edit_device_button.pack(side=tk.LEFT, padx=2)

        self.delete_device_button = ttk.Button(self.devices_buttons_frame, text="Удалить",
                                                command=self.delete_device)
        self.delete_device_button.pack(side=tk.LEFT, padx=2)

        # ---  Информация об устройстве ---
        self.device_info_label = ttk.Label(self.info_frame, text="Информация об устройстве:")
        self.device_info_label.pack(pady=2)

        self.device_type_label = ttk.Label(self.info_frame, text="Тип:")
        self.device_type_label.pack(pady=2)

        self.device_model_label = ttk.Label(self.info_frame, text="Модель:")
        self.device_model_label.pack(pady=2)

        self.device_serial_number_label = ttk.Label(self.info_frame, text="Серийный номер:")
        self.device_serial_number_label.pack(pady=2)

        self.device_inventory_number_label = ttk.Label(self.info_frame, text="Инвентарный номер:")
        self.device_inventory_number_label.pack(pady=2)

        self.device_cpu_label = ttk.Label(self.info_frame, text="CPU:")
        self.device_cpu_label.pack(pady=2)

        self.device_memory_label = ttk.Label(self.info_frame, text="Memory:")
        self.device_memory_label.pack(pady=2)

        self.device_hdd_label = ttk.Label(self.info_frame, text="HDD:")
        self.device_hdd_label.pack(pady=2)

        self.device_gpu_label = ttk.Label(self.info_frame, text="GPU:")
        self.device_gpu_label.pack(pady=2)

        self.device_status_label = ttk.Label(self.info_frame, text="Статус:")
        self.device_status_label.pack(pady=2)

        # ---  Периферия ---
        self.peripherals_label = ttk.Label(self.info_frame, text="Периферия:")
        self.peripherals_label.pack(pady=2)

        self.device_peripherals_tree = ttk.Treeview(self.info_frame, columns=("name", "type"), show="headings")
        self.device_peripherals_tree.heading("name", text="Название")
        self.device_peripherals_tree.heading("type", text="Тип")
        self.device_peripherals_tree.column("name", width=150)
        self.device_peripherals_tree.column("type", width=100)
        self.device_peripherals_tree.pack(fill="both", expand=True)
        self.device_peripherals_tree.bind("<ButtonRelease-1>", self.select_device_peripheral)

        # --- Кнопки управления периферией устройства ---
        self.device_peripherals_buttons_frame = ttk.Frame(self.info_frame)
        self.device_peripherals_buttons_frame.pack(pady=5)

        self.add_device_peripheral_button = ttk.Button(self.device_peripherals_buttons_frame, text="Добавить периферию", command=self.open_add_device_peripheral_window)
        self.add_device_peripheral_button.pack(side=tk.LEFT, padx=2)

        self.delete_device_peripheral_button = ttk.Button(self.device_peripherals_buttons_frame, text="Удалить периферию", command=self.delete_device_peripheral)
        self.delete_device_peripheral_button.pack(side=tk.LEFT, padx=2)

        # --- Инициализация выбранных элементов ---
        self.selected_department_id = None
        self.selected_device_id = None
        self.selected_device_peripheral_name = None

    # --- Функции для работы с отделами ---
    def load_departments(self):
        """Загружает список отделов в Treeview"""
        for item in self.departments_tree.get_children():
            self.departments_tree.delete(item)

        departments = database.get_departments()
        for department in departments:
            self.departments_tree.insert("", tk.END, values=(department[0], department[1]))

    def open_add_department_window(self):
        """Открывает окно для добавления отдела"""
        AddDepartmentWindow(self)

    def open_edit_department_window(self):
        """Открывает окно для редактирования отдела"""
        if self.selected_department_id:
            EditDepartmentWindow(self, self.selected_department_id)
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для редактирования.")

    def delete_department(self):
        """Удаляет выбранный отдел"""
        if self.selected_department_id:
            if messagebox.askyesno("Удаление отдела", "Вы уверены, что хотите удалить этот отдел?", parent=self):
                database.delete_department(self.selected_department_id)
                self.load_departments()
                self.clear_device_info()
                self.clear_department_info()
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для удаления.")

    def select_department(self, event):
        """Вызывается при выборе отдела в Treeview"""
        selected_item = self.departments_tree.selection()[0]  # Получаем ID выбранной строки
        self.selected_department_id = self.departments_tree.item(selected_item, 'values')[0]  # Получаем ID отдела
        department = database.get_departments(self.selected_department_id)

        # Отображаем информацию об отделе
        self.department_name_label.config(text=f"Название отдела: {department[1]}")

        # Загружаем компьютерную технику для выбранного отдела
        self.load_devices()

    def clear_department_info(self):
        """Очищает информацию об отделе"""
        self.department_name_label.config(text="Название отдела:")

    # --- Функции для работы с устройствами ---
    def load_devices(self):
        """Загружает список устройств в Treeview"""
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)

        if self.selected_department_id:
            devices = database.get_devices_by_department(self.selected_department_id)
            for device in devices:
                self.devices_tree.insert("", tk.END, values=(
                    device[0], device[2], device[3], device[4], device[5], device[6], device[7], device[8], device[9],
                    device[10]))
        else:
            self.clear_device_info()

    def open_add_device_window(self):
        """Открывает окно для добавления устройства"""
        if self.selected_department_id:
            AddDeviceWindow(self, self.selected_department_id)
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для добавления устройства.")

    def open_edit_device_window(self):
        """Открывает окно для редактирования устройства"""
        if self.selected_device_id:
            EditDeviceWindow(self, self.selected_device_id)
        else:
            messagebox.showinfo("Внимание", "Выберите устройство для редактирования.")

    def delete_device(self):
        """Удаляет выбранное устройство"""
        if self.selected_device_id:
            if messagebox.askyesno("Удаление устройства", "Вы уверены, что хотите удалить это устройство?", parent=self):
                database.delete_device(self.selected_device_id)
                self.load_devices()
                self.clear_device_info()
        else:
            messagebox.showinfo("Внимание", "Выберите устройство для удаления.")

    def select_device(self, event):
        """Вызывается при выборе устройства в Treeview"""
        selected_item = self.devices_tree.selection()[0]  # Получаем ID выбранной строки
        self.selected_device_id = self.devices_tree.item(selected_item, 'values')[0]  # Получаем ID устройства
        device = database.get_device(self.selected_device_id)

        # Отображаем информацию об устройстве
        self.device_type_label.config(text=f"Тип: {device[2]}")
        self.device_model_label.config(text=f"Модель: {device[3]}")
        self.device_serial_number_label.config(text=f"Серийный номер: {device[4]}")
        self.device_inventory_number_label.config(text=f"Инвентарный номер: {device[5]}")
        self.device_cpu_label.config(text=f"CPU: {device[6]}")
        self.device_memory_label.config(text=f"Memory: {device[7]}")
        self.device_hdd_label.config(text=f"HDD: {device[8]}")
        self.device_gpu_label.config(text=f"GPU: {device[9]}")
        self.device_status_label.config(text=f"Статус: {device[10]}")

        # Загружаем периферию для выбранного устройства
        self.load_device_peripherals()

    def clear_device_info(self):
        """Очищает информацию об устройстве"""
        self.device_type_label.config(text="Тип:")
        self.device_model_label.config(text="Модель:")
        self.device_serial_number_label.config(text="Серийный номер:")
        self.device_inventory_number_label.config(text="Инвентарный номер:")
        self.device_cpu_label.config(text="CPU:")
        self.device_memory_label.config(text="Memory:")
        self.device_hdd_label.config(text="HDD:")
        self.device_gpu_label.config(text="GPU:")
        self.device_status_label.config(text="Статус:")
        self.clear_device_peripherals()

    # --- Функции для работы с периферией ---
    def load_device_peripherals(self):
        """Загружает список периферии устройства в Treeview"""
        for item in self.device_peripherals_tree.get_children():
            self.device_peripherals_tree.delete(item)

        if self.selected_device_id:
            device_peripherals = database.get_device_peripherals(self.selected_device_id)
            for peripheral in device_peripherals:
                self.device_peripherals_tree.insert("", tk.END, values=(peripheral[0], peripheral[1]))
        else:
            self.clear_device_peripherals()

    def open_add_device_peripheral_window(self):
        """Открывает окно для добавления периферии к устройству"""
        if self.selected_device_id:
            AddDevicePeripheralWindow(self, self.selected_device_id)
        else:
            messagebox.showinfo("Внимание", "Выберите устройство для добавления периферии.")

    def delete_device_peripheral(self):
        """Удаляет выбранную периферию из устройства."""
        try:
            selected_item = self.device_peripherals_tree.selection()[0]
            peripheral_name = self.device_peripherals_tree.item(selected_item, 'values')[0]  # Получаем имя периферии
            peripheral = database.get_peripheral_by_name(peripheral_name)

            if peripheral is None:  # Добавлена проверка на None
                messagebox.showerror("Ошибка", "Периферийное устройство с именем '" + peripheral_name + "' не найдено.")
                return

            if messagebox.askyesno("Удаление периферии",
                                      "Вы уверены, что хотите удалить эту периферию из устройства?", parent=self):
                database.delete_device_peripheral(self.selected_device_id, peripheral[0])  # Исправлено на peripheral[0]
                self.load_device_peripherals()
        except IndexError:
            messagebox.showinfo("Внимание", "Выберите периферию для удаления.", parent=self)

    def clear_device_peripherals(self):
        """Очищает список периферии устройства"""
        for item in self.device_peripherals_tree.get_children():
            self.device_peripherals_tree.delete(item)

    def select_device_peripheral(self, event):
        """Вызывается при выборе периферии устройства в Treeview"""
        try:
            selected_item = self.device_peripherals_tree.selection()[0]
            self.selected_device_peripheral_name = self.device_peripherals_tree.item(selected_item, 'values')[0]
        except IndexError:
            self.selected_device_peripheral_name = None

    def open_peripherals_window(self):
        """Открывает окно для управления периферией"""
        PeripheralsWindow(self)

    # --- Отчетность ---
    def generate_report(self):
        """Генерирует отчет в окне Tkinter."""
        # 1. Получаем данные из базы данных
        departments = database.get_departments()  # Получаем все отделы
        if not departments:
            tk.messagebox.showinfo("Отчет", "Нет данных для создания отчета.")
            return

        # 2. Формируем текст отчета
        report_text = "Отчет о состоянии компьютерной техники по отделам:\n\n"
        for department in departments:
            report_text += f"Отдел: {department[1]} (ID: {department[0]})\n"  # Название отдела
            devices = database.get_devices_by_department(department[0])  # Получаем устройства для каждого отдела
            if devices:
                for device in devices:
                    report_text += f"  Устройство: {device[2]} {device[3]} (ID: {device[0]})\n"  # Тип и модель устройства
                    report_text += f"    Серийный номер: {device[4]}\n"
                    report_text += f"    Инв. номер: {device[5]}\n"
                    # Добавляем информацию о периферии
                    peripherals = database.get_device_peripherals(device[0])
                    if peripherals:
                        report_text += "    Периферия:\n"
                        for peripheral in peripherals:
                            report_text += f"      - {peripheral[0]} ({peripheral[1]})\n"
                    else:
                        report_text += "    Нет периферии.\n"
                    # ... (Добавьте другие параметры устройства по желанию)
                    report_text += "\n"
            else:
                report_text += "  В этом отделе нет устройств.\n\n"
            report_text += "\n"  # Добавляем разделитель между отделами

        # 3. Создаем новое окно для отчета
        report_window = tk.Toplevel(self)  # Передаем self в Toplevel
        report_window.title("Отчет")

        report_window.grid_rowconfigure(0, weight=1)
        report_window.grid_columnconfigure(0, weight=1)

        # 4. Добавляем текстовое поле для отображения отчета
        report_text_widget = tk.Text(report_window, wrap="word")  # wrap="word" для переноса слов
        report_text_widget.insert(tk.END, report_text)  # Вставляем текст в виджет
        report_text_widget.config(state="disabled")  # Делаем поле только для чтения, чтобы нельзя было редактировать
        report_text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # 5. Добавляем кнопку "Сохранить в файл" (необязательно)
        def save_report_to_file():
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if filepath:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(report_text)
                tk.messagebox.showinfo("Отчет", f"Отчет сохранен в файл: {filepath}")

        save_button = ttk.Button(report_window, text="Сохранить в файл", command=save_report_to_file)
        save_button.grid(row=1, column=0, pady=5)

    # ---  Запуск приложения ---
    def run(self):
        self.mainloop()


if __name__ == "__main__":
    database.create_tables()
    app = MainWindow()
    app.run()
