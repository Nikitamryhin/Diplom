import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font  # Импортируем font
from gui.add_device_window import AddDeviceWindow
from gui.edit_device_window import EditDeviceWindow
from gui.add_department_window import AddDepartmentWindow
from gui.add_employee_window import AddEmployeeWindow
from models.device import Device

class MainWindow:
    def __init__(self, root, db_connector):
        self.root = root
        self.root.title("Учет и контроль состояния компьютерной техники")

        # Устанавливаем минимальный размер окна
        self.root.minsize(800, 600)  # Ширина 800, высота 600

        self.db_connector = db_connector
        self.devices = []
        self.departments = []  # Добавим список отделов
        self.selected_department_id = None  # Добавляем переменную для хранения ID выбранного отдела
        self.department_buttons = {}  # Словарь для хранения кнопок отделов
        self.create_widgets()
        self.create_department_buttons()  # Создаем кнопки отделов

    def create_department_buttons(self):
        """Создает кнопки для каждого отдела."""
        departments = self.db_connector.fetch_all_departments()
        if departments:
            button_font = font.Font(size=8)  # Уменьшаем шрифт

            # Словари для хранения ID отделов
            department_ids = {}

            for i, department in enumerate(departments):
                # Сохраняем ID отдела в словаре
                department_ids[department.name] = department.id
                print(f"ID {department.name}: {department.id}")

                style = ttk.Style()
                style.configure("DepartmentButton.TButton", font=button_font)

                target_department_id = None

                if department.name == "Отдел тестирования" and "Отдел разработки" in department_ids:
                    target_department_id = department_ids["Отдел разработки"]
                    print(f"Кнопка Отдел тестирования переходит в Отдел разработки")
                elif department.name == "Отдел разработки" and "Отдел тестирования" in department_ids:
                    target_department_id = department_ids["Отдел тестирования"]
                    print(f"Кнопка Отдел разработки переходит в Отдел тестирования")
                elif department.name == "Отдел финансов" and "Отдел тестирования" in department_ids:
                    target_department_id = department_ids["Отдел тестирования"]
                    print(f"Кнопка Отдел финансов переходит в Отдел тестирования")  # Добавлено правило для отдела финансов
                else:
                    print(f"Для кнопки {department.name} не задан переход")

                button = ttk.Button(self.root, text=department.name, command=lambda dep=department: self.set_and_load_department(dep.id), style="DepartmentButton.TButton")
                button.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
                self.root.columnconfigure(i, weight=1)
                self.department_buttons[department.id] = (button, target_department_id)

    def set_and_load_department(self, department_id):
        """Устанавливает ID выбранного отдела и загружает данные."""
        self.selected_department_id = department_id
        self.load_department_data(department_id)

    def load_department_data(self, department_id):
        """Загружает данные для выбранного отдела."""
        self.load_employees(department_id)
        self.load_devices(department_id)
        # Здесь больше не нужно размещать виджеты.

        # Отображаем виджеты
        self.add_device_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")
        self.edit_device_button.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        self.delete_device_button.grid(row=1, column=2, pady=5, padx=5, sticky="ew")
        self.add_department_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")
        self.edit_department_button.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        self.delete_department_button.grid(row=2, column=2, pady=5, padx=5, sticky="ew")
        self.add_employee_button.grid(row=3, column=0, pady=5, padx=5, sticky="ew")
        self.delete_employee_button.grid(row=3, column=2, pady=5, padx=5, sticky="ew")
        self.go_button.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        self.tree.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.department_tree.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.employee_tree.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

    def create_widgets(self):
        # --- Кнопки управления устройствами ---
        self.add_device_button = ttk.Button(self.root, text="Добавить устройство", command=self.open_add_device_window)
        self.add_device_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        self.edit_device_button = ttk.Button(self.root, text="Редактировать устройство", command=self.open_edit_device_window)
        self.edit_device_button.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        self.delete_device_button = ttk.Button(self.root, text="Удалить устройство", command=self.delete_device)
        self.delete_device_button.grid(row=1, column=2, pady=5, padx=5, sticky="ew")

        # --- Кнопки управления отделами ---
        self.add_department_button = ttk.Button(self.root, text="Добавить отдел", command=self.open_add_department_window)
        self.add_department_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        self.edit_department_button = ttk.Button(self.root, text="Редактировать отдел", command=self.open_edit_department_window)
        self.edit_department_button.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        self.delete_department_button = ttk.Button(self.root, text="Удалить отдел", command=self.delete_department)
        self.delete_department_button.grid(row=2, column=2, pady=5, padx=5, sticky="ew")

        # --- Кнопки управления сотрудниками ---
        self.add_employee_button = ttk.Button(self.root, text="Добавить сотрудника", command=self.open_add_employee_window)
        self.add_employee_button.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        self.delete_employee_button = ttk.Button(self.root, text="Удалить сотрудника", command=self.delete_employee)
        self.delete_employee_button.grid(row=3, column=2, pady=5, padx=5, sticky="ew")

        # --- Кнопка "Перейти" ---
        self.go_button = ttk.Button(self.root, text="Перейти", command=self.go_to_selected)
        self.go_button.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        # --- Кнопка "Назад" ---
        self.back_button = ttk.Button(self.root, text="Назад", command=self.go_back, state=tk.DISABLED)
        self.back_button.grid(row=3, column=3, pady=5, padx=5, sticky="ew") # Разместите кнопку "Назад"

        self.back_button = ttk.Button(self.root, text="Назад", command=self.go_back, state=tk.DISABLED)
        self.back_button.grid(row=3, column=3, pady=5, padx=5, sticky="ew")

        # --- Treeview для устройств ---
        self.tree = ttk.Treeview(self.root, columns=("ID", "Название", "Категория", "Серийный номер", "Статус", "Отдел", "Ответственный"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Серийный номер", text="Серийный номер")
        self.tree.heading("Статус", text="Статус")
        self.tree.heading("Отдел", text="Отдел")
        self.tree.heading("Ответственный", text="Ответственный")
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # --- Treeview для отделов ---
        self.department_tree = ttk.Treeview(self.root, columns=("ID", "Название"), show="headings")
        self.department_tree.heading("ID", text="ID")
        self.department_tree.heading("Название", text="Название")
        self.department_tree.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # --- Treeview для сотрудников ---
        self.employee_tree = ttk.Treeview(self.root, columns=("ID", "Имя", "Должность"), show="headings")
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Имя", text="Имя")
        self.employee_tree.heading("Должность", text="Должность")
        self.employee_tree.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # --- Настройка строк и столбцов для правильного масштабирования ---
        # Установите вес только для тех строк и столбцов, которые должны расширяться.
        departments = self.db_connector.fetch_all_departments()
        if departments:
            for i in range(len(departments)):  # Чтобы кнопки отделов расширялись
                self.root.columnconfigure(i, weight=1)
        self.root.columnconfigure(3, weight=0) # Чтобы кнопка "Назад" не растягивалась
        self.root.rowconfigure(4, weight=1)  # Treeview для устройств
        self.root.rowconfigure(5, weight=1)  # Treeview для отделов
        self.root.rowconfigure(6, weight=1)  # Treeview для сотрудников

    def go_to_selected(self):
        """Выполняет переход к целевому отделу."""
        if self.selected_department_id:
            button, target_department_id = self.department_buttons.get(self.selected_department_id, (None, None))
            if target_department_id:
                self.load_department_data(target_department_id)
            else:
                tk.messagebox.showinfo("Информация", "Для этого отдела не задан целевой отдел для перехода.")
        else:
            tk.messagebox.showerror("Ошибка", "Выберите отдел для перехода.")

    def delete_employee(self):
        """Удаляет выбранного сотрудника."""
        selected_item = self.employee_tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите сотрудника для удаления.")
            return

        employee_id = self.employee_tree.item(selected_item[0])['values'][0]
        employee_name = self.employee_tree.item(selected_item[0])['values'][1]

        if tk.messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить сотрудника '{employee_name}'?"):
            try:
                self.db_connector.delete_employee(employee_id) # Вызываем метод для удаления сотрудника из базы данных
                self.load_employees() # Обновляем Treeview
                tk.messagebox.showinfo("Успех", "Сотрудник успешно удален.")
            except Exception as e:
                tk.messagebox.showerror("Ошибка", f"Ошибка при удалении сотрудника: {e}")

    def load_devices(self, department_id=None):
        """Загружает устройства из базы данных и отображает их в Treeview."""
        try:
            self.devices = self.db_connector.fetch_all_devices(department_id)
            # Очищаем Treeview перед загрузкой новых данных
            for item in self.tree.get_children():
                self.tree.delete(item)
            if not self.devices:
                self.tree.insert("", tk.END, values=("Нет устройств",))  # Отображаем сообщение
            else:
                for device in self.devices:
                    self.tree.insert("", tk.END, values=(device.id, device.name, device.category, device.serial_number, device.status, device.department_name, device.employee_name))
        except Exception as e:
            print(f"Error loading devices: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при загрузке устройств: {e}")

    def delete_device(self):
        """Удаляет выбранное устройство."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите устройство для удаления.")
            return

        device_id = self.tree.item(selected_item[0])['values'][0]

        try:
            # Подтверждаем удаление
            if tk.messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить это устройство?"):
                self.db_connector.delete_device(device_id)
                self.load_devices(self.selected_department_id)  # Обновляем список устройств
                tk.messagebox.showinfo("Успех", "Устройство успешно удалено.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при удалении устройства: {e}")

    def open_edit_device_window(self):
        """Открывает окно редактирования устройства."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите устройство для редактирования.")
            return

        device_id = self.tree.item(selected_item[0])['values'][0]

        try:
            # Получаем устройство из базы данных по ID
            devices = self.db_connector.fetch_all_devices()
            if not devices:  # Проверяем, есть ли устройства
                tk.messagebox.showerror("Ошибка", "Нет устройств для редактирования.")
                return
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
        """Удаляет выбранный отдел."""
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
        pass  # TODO

    def open_add_employee_window(self):
        """Открывает окно для добавления нового сотрудника."""
        AddEmployeeWindow(self.root, self.db_connector, self.load_employees, self.selected_department_id)

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

    def go_back(self):
        """Переходит к предыдущему отделу."""
        if self.department_history:
            previous_department_id = self.department_history.pop()
            self.set_and_load_department(previous_department_id)  # Directly call set_and_load_department
        self.update_back_button_state()

    def update_back_button_state(self):
        """Включает или выключает кнопку "Назад" в зависимости от истории."""
        if self.department_history:
            self.back_button.config(state=tk.NORMAL)  # Включаем кнопку, если есть история
        else:
            self.back_button.config(state=tk.DISABLED)  # Выключаем, если истории нет
