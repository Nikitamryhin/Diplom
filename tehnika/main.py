import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from db import database  # Используем from db import database
import sqlite3 # для get_device

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учет компьютерной техники")
        self.geometry("1152x850")

        # --- Переменные ---
        self.departments = database.get_departments()
        self.selected_department_id = None
        self.selected_device_id = None

        self.create_ui()
        self.load_departments()

    def create_ui(self):
        # --- Фрейм для списка отделов (слева) ---
        self.department_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.department_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        department_label = ttk.Label(self.department_frame, text="Название отдела")
        department_label.pack(pady=5)

        self.department_listbox = tk.Listbox(self.department_frame)
        self.department_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.department_listbox.bind("<<ListboxSelect>>", self.on_department_select)

        # Кнопки управления отделами
        self.department_buttons_frame = ttk.Frame(self.department_frame)
        self.department_buttons_frame.pack(pady=5)

        self.add_department_button = ttk.Button(self.department_buttons_frame, text="Добавить", command=self.add_department)
        self.add_department_button.pack(side=tk.LEFT, padx=2)

        self.delete_department_button = ttk.Button(self.department_buttons_frame, text="Удалить", command=self.delete_selected_department)
        self.delete_department_button.pack(side=tk.LEFT, padx=2)
        self.delete_department_button["state"] = tk.DISABLED

        # --- Фрейм для списка компьютеров (под списком отделов) ---
        self.computer_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.computer_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        computer_label = ttk.Label(self.computer_frame, text="Компьютерная техника в отделе")
        computer_label.pack(pady=5)

        self.computer_tree = ttk.Treeview(self.computer_frame,
                                         columns=("id", "type", "model", "serial", "inventory", "cpu", "memory", "hdd", "gpu", "status"), show="headings")
        self.computer_tree.pack(fill="both", expand=True, padx=5, pady=5)
        # Настройка заголовков столбцов
        self.computer_tree.heading("id", text="ID")
        self.computer_tree.heading("type", text="Тип")
        self.computer_tree.heading("model", text="Модель")
        self.computer_tree.heading("serial", text="Серийный номер")
        self.computer_tree.heading("inventory", text="Инв. номер")
        self.computer_tree.heading("cpu", text="CPU")
        self.computer_tree.heading("memory", text="Memory")
        self.computer_tree.heading("hdd", text="HDD")
        self.computer_tree.heading("gpu", text="GPU")
        self.computer_tree.heading("status", text="Статус")

        # Настройка ширины столбцов
        self.computer_tree.column("id", width=30)
        self.computer_tree.column("type", width=80)
        self.computer_tree.column("model", width=100)
        self.computer_tree.column("serial", width=100)
        self.computer_tree.column("inventory", width=80)
        self.computer_tree.column("cpu", width=100)
        self.computer_tree.column("memory", width=70)
        self.computer_tree.column("hdd", width=70)
        self.computer_tree.column("gpu", width=100)
        self.computer_tree.column("status", width=100)

        self.computer_tree.bind("<<TreeviewSelect>>", self.on_device_select)

        # Кнопки управления устройствами
        self.device_buttons_frame = ttk.Frame(self.computer_frame)
        self.device_buttons_frame.pack(pady=5)

        self.add_device_button = ttk.Button(self.device_buttons_frame, text="Добавить", command=self.add_device)
        self.add_device_button.pack(side=tk.LEFT, padx=2)

        self.delete_device_button = ttk.Button(self.device_buttons_frame, text="Удалить", command=self.delete_device)
        self.delete_device_button.pack(side=tk.LEFT, padx=2)
        self.delete_device_button["state"] = tk.DISABLED

        # --- Фрейм для информации о компьютере (справа) ---
        self.info_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.info_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)

        info_label = ttk.Label(self.info_frame, text="Информация о компьютере")
        info_label.pack(pady=5)

        # Поля для информации об устройстве
        self.type_label = ttk.Label(self.info_frame, text="Тип:")
        self.type_label.pack(pady=2)
        self.type_entry = ttk.Entry(self.info_frame)
        self.type_entry.pack(pady=2)

        self.model_label = ttk.Label(self.info_frame, text="Модель:")
        self.model_label.pack(pady=2)
        self.model_entry = ttk.Entry(self.info_frame)
        self.model_entry.pack(pady=2)

        self.serial_label = ttk.Label(self.info_frame, text="Серийный номер:")
        self.serial_label.pack(pady=2)
        self.serial_entry = ttk.Entry(self.info_frame)
        self.serial_entry.pack(pady=2)

        self.inventory_label = ttk.Label(self.info_frame, text="Инвентарный номер:")
        self.inventory_label.pack(pady=2)
        self.inventory_entry = ttk.Entry(self.info_frame)
        self.inventory_entry.pack(pady=2)

        self.cpu_label = ttk.Label(self.info_frame, text="CPU:")
        self.cpu_label.pack(pady=2)
        self.cpu_entry = ttk.Entry(self.info_frame)
        self.cpu_entry.pack(pady=2)

        self.memory_label = ttk.Label(self.info_frame, text="Memory:")
        self.memory_label.pack(pady=2)
        self.memory_entry = ttk.Entry(self.info_frame)
        self.memory_entry.pack(pady=2)

        self.hdd_label = ttk.Label(self.info_frame, text="HDD:")
        self.hdd_label.pack(pady=2)
        self.hdd_entry = ttk.Entry(self.info_frame)
        self.hdd_entry.pack(pady=2)

        self.gpu_label = ttk.Label(self.info_frame, text="GPU:")
        self.gpu_label.pack(pady=2)
        self.gpu_entry = ttk.Entry(self.info_frame)
        self.gpu_entry.pack(pady=2)

        self.status_label = ttk.Label(self.info_frame, text="Статус:")
        self.status_label.pack(pady=2)
        self.status_entry = ttk.Entry(self.info_frame)
        self.status_entry.pack(pady=2)

        self.save_button = ttk.Button(self.info_frame, text="Сохранить изменения", command=self.save_device)
        self.save_button.pack(pady=10)
        self.save_button["state"] = tk.DISABLED

        # --- Menu ---
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Управление расходными материалами", command=self.open_consumables_window) # Добавляем пункт в меню
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.config(menu=menubar)

        # ---  Расходные материалы ---
        self.consumables_label = ttk.Label(self.info_frame, text="Расходные материалы:")
        self.consumables_label.pack(pady=2)

        self.device_consumables_tree = ttk.Treeview(self.info_frame, columns=("id", "name", "quantity"), show="headings")
        self.device_consumables_tree.heading("id", text="ID")
        self.device_consumables_tree.heading("name", text="Название")
        self.device_consumables_tree.heading("quantity", text="Количество")
        self.device_consumables_tree.pack(fill="x", padx=5, pady=5)

        self.add_consumable_button = ttk.Button(self.info_frame, text="Добавить расходный материал", command=self.add_device_consumable)
        self.add_consumable_button.pack(pady=2)

        # --- Настройка размеров строк и столбцов ---
        self.grid_columnconfigure(0, weight=1)  # Список отделов и компьютеров расширяются
        self.grid_columnconfigure(1, weight=2)  # Информация о компьютере занимает больше места
        self.grid_rowconfigure(0, weight=1)     # Список отделов и информация расширяются по вертикали
        self.grid_rowconfigure(1, weight=1)     # Список компьютеров расширяются по вертикали

    def open_consumables_window(self):
         self.consumables_window = ConsumablesWindow(self) # Создаём окно расходных материалов

    def load_departments(self):
        """Загружает список отделов в Listbox"""
        self.department_listbox.delete(0, tk.END)
        self.departments = database.get_departments()
        for department in self.departments:
            self.department_listbox.insert(tk.END, department[1])

    def load_devices(self):
        """Загружает список устройств в Treeview"""
        for item in self.computer_tree.get_children():
            self.computer_tree.delete(item)

        if self.selected_department_id:
            devices = database.get_devices(self.selected_department_id)
            for device in devices:
                self.computer_tree.insert("", tk.END, values=(device[0], device[2], device[3], device[4], device[5],
                                                             device[6], device[7], device[8], device[9], device[10]))

    def load_device_info(self):
      if self.selected_device_id:
            device = database.get_device(self.selected_device_id)  # Предполагаем, что у вас есть такая функция
            if device:
                self.type_entry.delete(0, tk.END)
                self.type_entry.insert(0, device[2])
                self.model_entry.delete(0, tk.END)
                self.model_entry.insert(0, device[3])
                self.serial_entry.delete(0, tk.END)
                self.serial_entry.insert(0, device[4])
                self.inventory_entry.delete(0, tk.END)
                self.inventory_entry.insert(0, device[5])
                self.cpu_entry.delete(0, tk.END)
                self.cpu_entry.insert(0, device[6])
                self.memory_entry.delete(0, tk.END)
                self.memory_entry.insert(0, device[7])
                self.hdd_entry.delete(0, tk.END)
                self.hdd_entry.insert(0, device[8])
                self.gpu_entry.delete(0, tk.END)
                self.gpu_entry.insert(0, device[9])
                self.status_entry.delete(0, tk.END)
                self.status_entry.insert(0, device[10])

                self.save_button["state"] = tk.NORMAL  # Включаем кнопку "Сохранить"
                self.load_device_consumables() # Загружаем расходные материалы для устройства
            else:
                self.clear_device_info()

    def load_device_consumables(self):
        """Загружает список расходных материалов для устройства"""
        for item in self.device_consumables_tree.get_children():
            self.device_consumables_tree.delete(item)

        if self.selected_device_id:
            device_consumables = database.get_device_consumables(self.selected_device_id)
            for dc in device_consumables:
                self.device_consumables_tree.insert("", tk.END, values=(dc[0], dc[1], dc[2]))

    def clear_device_info(self):
        """Очищает поля информации об устройстве"""
        self.type_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.serial_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)
        self.cpu_entry.delete(0, tk.END)
        self.memory_entry.delete(0, tk.END)
        self.hdd_entry.delete(0, tk.END)
        self.gpu_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.save_button["state"] = tk.DISABLED
        self.clear_device_consumables()

    def clear_device_consumables(self):
         for item in self.device_consumables_tree.get_children():
            self.device_consumables_tree.delete(item)

    def add_department(self):
        """Добавляет новый отдел."""
        name = simpledialog.askstring("Добавить отдел", "Введите название отдела:", parent=self)
        if name:
            department_id = database.insert_department(name)
            self.load_departments()
            self.department_listbox.selection_set(tk.END)
            self.on_department_select(None) # Вызываем событие выбора, чтобы сразу загрузить устройства

    def delete_selected_department(self):
        """Удаляет выбранный отдел."""
        if self.selected_department_id is not None:
            if messagebox.askyesno("Удаление отдела", "Вы уверены, что хотите удалить этот отдел?", parent=self):
                database.delete_department(self.selected_department_id)
                self.load_departments()
                self.load_devices()
                self.clear_device_info()
                self.selected_department_id = None
                self.selected_device_id = None
                self.delete_department_button["state"] = tk.DISABLED  # Отключаем кнопку
                self.delete_device_button["state"] = tk.DISABLED
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для удаления.", parent=self)

    def add_device(self):
        """Добавляет новое устройство в выбранный отдел."""
        if self.selected_department_id:
            device_type = simpledialog.askstring("Добавить устройство", "Введите тип устройства (ПК, ноутбук и т.д.):", parent=self)
            model = simpledialog.askstring("Добавить устройство", "Введите модель устройства:", parent=self)
            serial_number = simpledialog.askstring("Добавить устройство", "Введите серийный номер устройства:",
                                                     parent=self)
            inventory_number = simpledialog.askstring("Добавить устройство", "Введите инвентарный номер устройства:",
                                                       parent=self)
            cpu = simpledialog.askstring("Добавить устройство", "Введите процессор:", parent=self)
            memory = simpledialog.askstring("Добавить устройство", "Введите объем памяти:", parent=self)
            hard_drive = simpledialog.askstring("Добавить устройство", "Введите объем жесткого диска:", parent=self)
            video_card = simpledialog.askstring("Добавить устройство", "Введите видеокарту:", parent=self)
            status = simpledialog.askstring("Добавить устройство", "Введите статус устройства:", parent=self)
            if device_type and model and serial_number and inventory_number and cpu and memory and hard_drive and video_card and status:
                device_id = database.insert_device(self.selected_department_id, device_type, model, serial_number,
                                                      inventory_number, cpu, memory, hard_drive, video_card, status)
                self.load_devices()
                # Select the newly added device
                for item in self.computer_tree.get_children():
                    if self.computer_tree.item(item)['values'][0] == device_id:
                        self.computer_tree.selection_set(item)
                        self.computer_tree.focus(item)
                        self.on_device_select(None)
                        break
        else:
            messagebox.showinfo("Внимание", "Выберите отдел для добавления устройства.", parent=self)

    def delete_device(self):
        """Удаляет выбранное устройство."""
        if self.selected_device_id:
            if messagebox.askyesno("Удаление устройства", "Вы уверены, что хотите удалить это устройство?",
                                      parent=self):
                database.delete_device(self.selected_device_id)
                self.load_devices()
                self.clear_device_info()
                self.selected_device_id = None
                self.delete_device_button["state"] = tk.DISABLED
        else:
            messagebox.showinfo("Внимание", "Выберите устройство для удаления.", parent=self)

    def save_device(self):
        """Сохраняет изменения информации об устройстве."""
        if self.selected_device_id:
            device_type = self.type_entry.get()
            model = self.model_entry.get()
            serial_number = self.serial_entry.get()
            inventory_number = self.inventory_entry.get()
            cpu = self.cpu_entry.get()
            memory = self.memory_entry.get()
            hard_drive = self.hdd_entry.get()
            gpu = self.gpu_entry.get()
            status = self.status_entry.get()

            database.update_device(self.selected_device_id, self.selected_department_id, device_type, model,
                                      serial_number, inventory_number, cpu, memory, hard_drive, gpu, status)
            self.load_devices()  # Обновляем список устройств
        else:
            messagebox.showinfo("Внимание", "Выберите устройство для сохранения.", parent=self)

    def on_department_select(self, event):
        """Обрабатывает выбор отдела в Listbox"""
        try:
            selected_index = self.department_listbox.curselection()[0]
            self.selected_department_id = self.departments[selected_index][0]
            self.load_devices()
            self.clear_device_info()
            self.delete_department_button["state"] = tk.NORMAL
            self.delete_device_button["state"] = tk.DISABLED
        except IndexError:
            self.clear_device_info()
            self.selected_department_id = None
            self.delete_department_button["state"] = tk.DISABLED
            self.delete_device_button["state"] = tk.DISABLED

    def on_device_select(self, event):
        """Обрабатывает выбор устройства в Treeview"""
        try:
            selected_item = self.computer_tree.selection()[0]
            self.selected_device_id = self.computer_tree.item(selected_item)['values'][0]
            self.load_device_info()
            self.delete_device_button["state"] = tk.NORMAL
        except IndexError:
            self.clear_device_info()
            self.selected_device_id = None
            self.delete_device_button["state"] = tk.DISABLED

    def add_device_consumable(self):
          if self.selected_device_id:
            AddDeviceConsumableDialog(self, self.selected_device_id)
          else:
            messagebox.showinfo("Внимание", "Выберите устройство, чтобы добавить расходный материал.", parent=self)


# --- Диалоговые окна для добавления и редактирования расходных материалов ---
class ConsumablesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Управление расходными материалами")
        self.geometry("600x400")

        self.create_ui()
        self.load_consumables()

    def create_ui(self):
        self.consumables_tree = ttk.Treeview(self, columns=("id", "name", "quantity", "price", "description"),
                                                show="headings")
        self.consumables_tree.heading("id", text="ID")
        self.consumables_tree.heading("name", text="Название")
        self.consumables_tree.heading("quantity", text="Количество")
        self.consumables_tree.heading("price", text="Цена")
        self.consumables_tree.heading("description", text="Описание")
        self.consumables_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Кнопки управления
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(pady=5)

        self.add_button = ttk.Button(self.buttons_frame, text="Добавить", command=self.add_consumable)
        self.add_button.pack(side=tk.LEFT, padx=2)

        self.edit_button = ttk.Button(self.buttons_frame, text="Редактировать", command=self.edit_consumable)
        self.edit_button.pack(side=tk.LEFT, padx=2)

        self.delete_button = ttk.Button(self.buttons_frame, text="Удалить", command=self.delete_consumable)
        self.delete_button.pack(side=tk.LEFT, padx=2)

    def load_consumables(self):
        """Загружает список расходных материалов в Treeview"""
        for item in self.consumables_tree.get_children():
            self.consumables_tree.delete(item)

        consumables = database.get_consumables()
        for consumable in consumables:
            self.consumables_tree.insert("", tk.END, values=consumable)

    def add_consumable(self):
        """Добавляет новый расходный материал."""
        AddConsumableDialog(self)

    def edit_consumable(self):
        """Редактирует выбранный расходный материал."""
        try:
            selected_item = self.consumables_tree.selection()[0]
            consumable_id = self.consumables_tree.item(selected_item)['values'][0]
            EditConsumableDialog(self, consumable_id)
        except IndexError:
            messagebox.showinfo("Внимание", "Выберите расходный материал для редактирования.", parent=self)

    def delete_consumable(self):
        """Удаляет выбранный расходный материал."""
        try:
            selected_item = self.consumables_tree.selection()[0]
            consumable_id = self.consumables_tree.item(selected_item)['values'][0]
            if messagebox.askyesno("Удаление расходного материала",
                                      "Вы уверены, что хотите удалить этот расходный материал?", parent=self):
                database.delete_consumable(consumable_id)
                self.load_consumables()
        except IndexError:
            messagebox.showinfo("Внимание", "Выберите расходный материал для удаления.", parent=self)

# --- Диалоговые окна для добавления и редактирования расходных материалов ---
class AddConsumableDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, title="Добавить расходный материал")

    def body(self, master):
        ttk.Label(master, text="Название:").grid(row=0, sticky=tk.W)
        self.name_entry = ttk.Entry(master)
        self.name_entry.grid(row=0, column=1, sticky=tk.E)

        ttk.Label(master, text="Количество:").grid(row=1, sticky=tk.W)
        self.quantity_entry = ttk.Entry(master)
        self.quantity_entry.grid(row=1, column=1, sticky=tk.E)

        ttk.Label(master, text="Цена:").grid(row=2, sticky=tk.W)
        self.price_entry = ttk.Entry(master)
        self.price_entry.grid(row=2, column=1, sticky=tk.E)

        ttk.Label(master, text="Описание:").grid(row=3, sticky=tk.W)
        self.description_entry = ttk.Entry(master)
        self.description_entry.grid(row=3, column=1, sticky=tk.E)

        return self.name_entry

    def apply(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        description = self.description_entry.get()

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные значения для количества или цены.")
            return

        database.insert_consumable(name, quantity, price, description)
        self.parent.load_consumables()


class EditConsumableDialog(simpledialog.Dialog):
    def __init__(self, parent, consumable_id):
        self.parent = parent
        self.consumable_id = consumable_id
        super().__init__(parent, title="Редактировать расходный материал")

    def body(self, master):
        # Загружаем информацию о расходном материале
        consumable = database.get_consumable(self.consumable_id)
        if not consumable:
            messagebox.showerror("Ошибка", "Расходный материал не найден.")
            self.destroy()
            return

        ttk.Label(master, text="Название:").grid(row=0, sticky=tk.W)
        self.name_entry = ttk.Entry(master)
        self.name_entry.insert(0, consumable[1])
        self.name_entry.grid(row=0, column=1, sticky=tk.E)

        ttk.Label(master, text="Количество:").grid(row=1, sticky=tk.W)
        self.quantity_entry = ttk.Entry(master)
        self.quantity_entry.insert(0, consumable[2])
        self.quantity_entry.grid(row=1, column=1, sticky=tk.E)

        ttk.Label(master, text="Цена:").grid(row=2, sticky=tk.W)
        self.price_entry = ttk.Entry(master)
        self.price_entry.insert(0, consumable[3])
        self.price_entry.grid(row=2, column=1, sticky=tk.E)

        ttk.Label(master, text="Описание:").grid(row=3, sticky=tk.W)
        self.description_entry = ttk.Entry(master)
        self.description_entry.insert(0, consumable[4])
        self.description_entry.grid(row=3, column=1, sticky=tk.E)

        return self.name_entry

    def apply(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        description = self.description_entry.get()

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные значения для количества или цены.")
            return

        database.update_consumable(self.consumable_id, name, quantity, price, description)
        self.parent.load_consumables()

class AddDeviceConsumableDialog(simpledialog.Dialog):
    def __init__(self, parent, device_id):
        self.parent = parent
        self.device_id = device_id
        super().__init__(parent, title="Добавить расходный материал к устройству")

    def body(self, master):
        ttk.Label(master, text="Расходный материал:").grid(row=0, sticky=tk.W)
        self.consumable_combobox = ttk.Combobox(master, state="normal")
        self.consumable_combobox.grid(row=0, column=1, sticky=tk.E)

        ttk.Label(master, text="Количество:").grid(row=1, sticky=tk.W)
        self.quantity_entry = ttk.Entry(master)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=1, column=1, sticky=tk.E)

        return self.consumable_combobox

    def apply(self):
        consumables = database.get_consumables()
        selected_index = self.consumable_combobox.current()
        if selected_index >= 0 and selected_index < len(consumables):
            consumable_id = consumables[selected_index][0]
            quantity = self.quantity_entry.get()

            try:
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректное значение для количества.")
                return

            database.insert_device_consumable(self.device_id, consumable_id, quantity)
            self.parent.load_device_consumables()
        else:
            messagebox.showerror("Ошибка", "Выберите расходный материал.")

# Предполагаем, что у вас есть функция get_device в database.py:
def get_device(id):
    connection = sqlite3.connect('demo.db')  # Замените 'demo.db' на имя вашей базы данных
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Devices WHERE id=?", (id,))
    device = cursor.fetchone()
    connection.close()
    return device


# Добавляем функцию get_device в класс database
database.get_device = get_device

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()