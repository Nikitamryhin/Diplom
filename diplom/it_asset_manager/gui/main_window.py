import tkinter as tk
from tkinter import ttk, font, messagebox
from gui.add_department_window import AddDepartmentWindow
from gui.edit_department_window import EditDepartmentWindow
from gui.add_device_window import AddDeviceWindow
from gui.edit_device_window import EditDeviceWindow
from gui.add_employee_window import AddEmployeeWindow
from gui.edit_employee_window import EditEmployeeWindow
from models.department import Department


class MainWindow:
    def __init__(self, root, db_connector):
        self.root = root
        self.db_connector = db_connector
        self.root.title("IT Asset Manager")
        self.root.geometry("1200x600")
        self.root.minsize(900, 400)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.selected_department_id = None
        self.department_history = []
        self.department_buttons = {}

        # Верхняя рамка для кнопок отделов
        self.department_frame = ttk.Frame(self.root, padding=10)
        self.department_frame.grid(row=0, column=0, sticky="ew")

        # Кнопка "Назад"
        self.back_button = ttk.Button(self.department_frame, text="Назад", command=self.go_back, state="disabled")
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Кнопка "Обновить"
        self.refresh_button = ttk.Button(self.department_frame, text="Обновить", command=self.refresh_data)
        self.refresh_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Рамка для Treeview и кнопок управления
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=1, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Treeview для отображения устройств
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Category", "Serial Number", "Status", "Department", "Employee"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Serial Number", text="Serial Number")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Employee", text="Employee")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", self.open_edit_device_window)

        # Treeview для отображения сотрудников
        self.employee_tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Position"), show="headings")
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Name", text="Name")
        self.employee_tree.heading("Position", text="Position")
        self.employee_tree.grid(row=0, column=1, sticky="nsew")
        self.employee_tree.bind("<Double-1>", self.open_edit_employee_window)

        # Scrollbar для Treeview устройств
        self.tree_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=0, column=0, sticky="nse")

        # Scrollbar для Treeview сотрудников
        self.employee_tree_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.employee_tree.yview)
        self.employee_tree.configure(yscrollcommand=self.employee_tree_scrollbar.set)
        self.employee_tree_scrollbar.grid(row=0, column=1, sticky="nse")

        # Нижняя рамка для кнопок управления
        self.button_frame = ttk.Frame(self.main_frame, padding=10)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Кнопки для управления устройствами
        self.add_device_button = ttk.Button(self.button_frame, text="Добавить устройство", command=self.open_add_device_window)
        self.add_device_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.edit_device_button = ttk.Button(self.button_frame, text="Редактировать устройство", command=self.open_edit_device_window)
        self.edit_device_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.delete_device_button = ttk.Button(self.button_frame, text="Удалить устройство", command=self.delete_device)
        self.delete_device_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

         # Кнопки для управления отделами
        self.add_department_button = ttk.Button(self.button_frame, text="Добавить отдел", command=self.open_add_department_window)
        self.add_department_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.edit_department_button = ttk.Button(self.button_frame, text="Редактировать отдел", command=self.open_edit_department_window)
        self.edit_department_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.delete_department_button = ttk.Button(self.button_frame, text="Удалить отдел", command=self.delete_department)
        self.delete_department_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Кнопки для управления сотрудниками
        self.add_employee_button = ttk.Button(self.button_frame, text="Добавить сотрудника", command=self.open_add_employee_window)
        self.add_employee_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.edit_employee_button = ttk.Button(self.button_frame, text="Редактировать сотрудника", command=self.open_edit_employee_window)
        self.edit_employee_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.delete_employee_button = ttk.Button(self.button_frame, text="Удалить сотрудника", command=self.delete_employee)
        self.delete_employee_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Разделитель между кнопками управления устройствами и сотрудников
        self.separator = ttk.Separator(self.button_frame, orient="vertical")
        self.separator.grid(row=0, column=3, rowspan=3, sticky="ns", padx=10)

        # Кнопка "Выход"
        self.exit_button = ttk.Button(self.button_frame, text="Выход", command=root.destroy)
        self.exit_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

        # Заполнение данными
        self.create_department_buttons()
        self.load_employees()
        self.load_devices()

    def load_department_data(self, department_id):
        """Загружает данные для выбранного отдела."""
        self.load_employees(department_id)
        self.load_devices(department_id)

    def load_employees(self, department_id=None):
        """Загружает сотрудников из базы данных и отображает их в Treeview."""
        try:
            employees = self.db_connector.fetch_all_employees(department_id)
            # Очищаем Treeview перед загрузкой новых данных
            for item in self.employee_tree.get_children():
                self.employee_tree.delete(item)
            for employee in employees:
                self.employee_tree.insert("", tk.END, values=(employee.id, employee.name, employee.position))
        except Exception as e:
            print(f"Error loading employees: {e}")
            messagebox.showerror("Ошибка", f"Ошибка при загрузке сотрудников: {e}")

    def load_devices(self, department_id=None):
        """Загружает устройства из базы данных и отображает их в Treeview."""
        try:
            if department_id is None:
                self.devices = self.db_connector.fetch_all_devices()
            else:
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

                button = ttk.Button(self.department_frame, text=department.name, command=lambda dep=department: self.set_and_load_department(dep.id), style="DepartmentButton.TButton")
                button.grid(row=1, column=i+2, padx=2, pady=2, sticky="ew")  # Смещаем кнопки вправо
                self.department_frame.columnconfigure(i+2, weight=1)
                self.department_buttons[department.id] = (button, target_department_id)

    def set_and_load_department(self, department_id):
        """Устанавливает ID выбранного отдела и загружает данные."""
        if self.selected_department_id is not None:
            self.department_history.append(self.selected_department_id)  # Добавляем текущий отдел в историю
        self.selected_department_id = department_id
        self.load_department_data(department_id)
        self.update_back_button_state() # Обновляем состояние кнопки "Назад"

    def go_back(self):
        """Возвращает к предыдущему отделу."""
        if self.department_history:
            previous_department_id = self.department_history.pop()
            self.set_and_load_department(previous_department_id)
        self.update_back_button_state()

    def update_back_button_state(self):
        """Обновляет состояние кнопки 'Назад'."""
        self.back_button["state"] = "normal" if self.department_history else "disabled"

    def open_add_device_window(self):
        """Открывает окно для добавления нового устройства."""
        AddDeviceWindow(self.root, self.db_connector, self.load_devices, self.selected_department_id)

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

    def open_add_department_window(self):
         """Открывает окно для добавления нового отдела."""
         AddDepartmentWindow(self.root, self.db_connector, self.create_department_buttons)

    def open_edit_department_window(self):
        """Открывает окно редактирования отдела."""
        selected_item = self.department_frame.winfo_children()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите отдел для редактирования.")
            return
        departments = self.db_connector.fetch_all_departments()
        department_id = departments[0].id

        try:
            # Получаем отдел из базы данных по ID
            departments = self.db_connector.fetch_all_departments()
            if not departments:  # Проверяем, есть ли отделы
                tk.messagebox.showerror("Ошибка", "Нет отделов для редактирования.")
                return
        # department = next((d for d in departments if d.id == department_id), None)
            department = departments[0]
            if department:
                edit_window = EditDepartmentWindow(self.root, self.db_connector, department, self.create_department_buttons)
            else:
                tk.messagebox.showerror("Ошибка", "Отдел не найден.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при открытии окна редактирования: {e}")

    def delete_department(self):
        """Удаляет выбранный отдел."""
        selected_item = self.department_frame.winfo_children()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите отдел для удаления.")
            return
        departments = self.db_connector.fetch_all_departments()
        department_id = departments[0].id

        try:
            # Подтверждаем удаление
            if tk.messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот отдел?"):
                self.db_connector.delete_department(department_id)
                self.create_department_buttons()  # Обновляем список отделов
                tk.messagebox.showinfo("Успех", "Отдел успешно удален.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при удалении отдела: {e}")

    def open_edit_employee_window(self):
        """Открывает окно редактирования сотрудника."""
        selected_item = self.employee_tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите сотрудника для редактирования.")
            return

        employee_id = self.employee_tree.item(selected_item[0])['values'][0]

        try:
            # Получаем сотрудника из базы данных по ID
            employees = self.db_connector.fetch_all_employees(self.selected_department_id) # Исправлено
            if not employees:  # Проверяем, есть ли сотрудники
                tk.messagebox.showerror("Ошибка", "Нет сотрудников для редактирования.")
                return
            employee = next((e for e in employees if e.id == employee_id), None)

            if employee:
                edit_window = EditEmployeeWindow(self.root, self.db_connector, employee, self.load_employees)
            else:
                tk.messagebox.showerror("Ошибка", "Сотрудник не найден.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при открытии окна редактирования: {e}")


    def open_edit_employee_window(self):
        """Открывает окно редактирования сотрудника."""
        selected_item = self.employee_tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите сотрудника для редактирования.")
            return

        employee_id = self.employee_tree.item(selected_item[0])['values'][0]

        try:
            # Получаем сотрудника из базы данных по ID
            employees = self.db_connector.fetch_all_employees()
            if not employees:  # Проверяем, есть ли сотрудники
                tk.messagebox.showerror("Ошибка", "Нет сотрудников для редактирования.")
                return
            employee = next((e for e in employees if e.id == employee_id), None)

            if employee:
                edit_window = EditEmployeeWindow(self.root, self.db_connector, employee, self.load_employees)
            else:
                tk.messagebox.showerror("Ошибка", "Сотрудник не найден.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при открытии окна редактирования: {e}")

    def delete_employee(self):
        """Удаляет выбранного сотрудника."""
        selected_item = self.employee_tree.selection()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Выберите сотрудника для удаления.")
            return

        employee_id = self.employee_tree.item(selected_item[0])['values'][0]

        try:
            # Подтверждаем удаление
            if tk.messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого сотрудника?"):
                self.db_connector.delete_employee(employee_id)
                self.load_employees(self.selected_department_id)  # Обновляем список сотрудников
                tk.messagebox.showinfo("Успех", "Сотрудник успешно удален.")
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при удалении сотрудника: {e}")

    def refresh_data(self):
         """Обновляет данные в Treeview."""
         if self.selected_department_id is not None:
             self.load_department_data(self.selected_department_id)
         else:
             self.load_employees()
             self.load_devices()
         self.create_department_buttons()
