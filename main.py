import csv
import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkinter import filedialog
import tkinter.font as tkFont
from db import database
from styles import configure_styles  # Убедитесь, что путь к файлу database.py указан верно

class RegisterDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.parent = parent
        self.roles = ["user", "admin"]  # Define available roles
        super().__init__(parent, title="Регистрация")

    def body(self, master):
        ttk.Label(master, text="Логин:", style="TLabel").grid(row=0)
        self.username_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.username_entry.grid(row=0, column=1)

        ttk.Label(master, text="Пароль:", style="TLabel").grid(row=1)
        self.password_entry = ttk.Entry(master, show="*", style="TEntry")  # Применяем стиль
        self.password_entry.grid(row=1, column=1)

        ttk.Label(master, text="Роль:", style="TLabel").grid(row=2)
        self.role_combobox = ttk.Combobox(master, values=self.roles, state="readonly", style="TCombobox")  # Применяем стиль
        self.role_combobox.set("user")  # Default role
        self.role_combobox.grid(row=2, column=1)

        return self.username_entry  # initial focus

    def apply(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()

        if username and password:
            hashed_password = database.hash_password(password)
            database.insert_user(username, hashed_password, role)
            messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован.")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля.")

class LoginDialog(simpledialog.Dialog):
    def __init__(self, parent, users):
        self.parent = parent
        self.users = users
        super().__init__(parent, title="Вход")

    def body(self, master):
        # Выпадающий список для выбора пользователя
        ttk.Label(master, text="Выберите пользователя:", style="TLabel").grid(row=0)
        self.user_combobox = ttk.Combobox(master, values=[user[1] for user in self.users], state="readonly", style="TCombobox")  # Применяем стиль
        self.user_combobox.grid(row=0, column=1)

        # Поле для ввода пароля
        ttk.Label(master, text="Пароль:", style="TLabel").grid(row=1)
        self.password_entry = ttk.Entry(master, show="*", style="TEntry")  # Применяем стиль
        self.password_entry.grid(row=1, column=1)

        return self.user_combobox  # initial focus

    def apply(self):
        selected_username = self.user_combobox.get()
        password = self.password_entry.get()

        if selected_username and password:
            # Находим выбранного пользователя в списке
            selected_user = next((user for user in self.users if user[1] == selected_username), None)
            if selected_user:
                # Проверяем пароль
                if database.verify_password(password, selected_user[2]):
                    self.parent.current_user = selected_user
                    self.parent.enable_menu()
                    self.parent.update_user_label()
                    messagebox.showinfo("Успех", "Вход выполнен.")
                else:
                    messagebox.showerror("Ошибка", "Неверный пароль.")
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден.")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля.")

class CustomerFrame(ttk.Frame):
    def __init__(self, parent, main_font):
        super().__init__(parent)
        self.parent = parent
        self.main_font = main_font
        self.selected_customer_id = None
        self.create_widgets()
        self.load_customers()

    def create_widgets(self):
        # --- Treeview для отображения списка клиентов ---
        self.customer_tree = ttk.Treeview(self, columns=("CustomerID", "CustomerType", "FirstName", "LastName", "CompanyName", "ContactName", "Email", "Phone", "Address", "RegistrationDate", "Notes"), show="headings")  # Убрали City, Region
        self.customer_tree.heading("CustomerID", text="ID")
        self.customer_tree.heading("CustomerType", text="Тип")
        self.customer_tree.heading("FirstName", text="Имя")
        self.customer_tree.heading("LastName", text="Фамилия")
        self.customer_tree.heading("CompanyName", text="Компания")
        self.customer_tree.heading("ContactName", text="Контактное лицо")
        self.customer_tree.heading("Email", text="Email")
        self.customer_tree.heading("Phone", text="Телефон")
        self.customer_tree.heading("Address", text="Адрес")
        self.customer_tree.heading("RegistrationDate", text="Дата регистрации")
        self.customer_tree.heading("Notes", text="Заметки")

        #  Настройка ширины столбцов
        self.customer_tree.column("CustomerID", width=30)
        self.customer_tree.column("CustomerType", width=80)
        self.customer_tree.column("FirstName", width=100)
        self.customer_tree.column("LastName", width=100)
        self.customer_tree.column("CompanyName", width=150)
        self.customer_tree.column("ContactName", width=150)
        self.customer_tree.column("Email", width=150)
        self.customer_tree.column("Phone", width=100)
        self.customer_tree.column("Address", width=150)
        self.customer_tree.column("RegistrationDate", width=100)
        self.customer_tree.column("Notes", width=200)

        self.customer_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.customer_tree.bind("<<TreeviewSelect>>", self.on_customer_select)

        # --- Фрейм для фильтров ---
        self.filter_frame = ttk.Frame(self)
        self.filter_frame.pack(pady=5)

        # --- Метка и Combobox для выбора типа клиента ---
        self.customer_type_label = ttk.Label(self.filter_frame, text="Тип клиента:", style="TLabel")
        self.customer_type_label.pack(side="left", padx=2)
        self.customer_type_options = ["Все", "Физическое лицо", "Юридическое лицо"]
        self.customer_type_str = tk.StringVar(value="Все")
        self.customer_type_combobox = ttk.Combobox(self.filter_frame, textvariable=self.customer_type_str, values=self.customer_type_options, state="readonly", style="TCombobox") # Применяем стиль
        self.customer_type_combobox.pack(side="left", padx=2)
        self.customer_type_combobox.bind("<<ComboboxSelected>>", self.apply_filter) #  Добавляем обработчик события

        # --- Кнопки управления клиентами ---
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(pady=5)

        self.add_button = ttk.Button(self.buttons_frame, text="Добавить", command=self.add_customer, style="TButton")  # Применяем стиль
        self.add_button.pack(side=tk.LEFT, padx=2)

        self.edit_button = ttk.Button(self.buttons_frame, text="Редактировать", command=self.edit_customer, state=tk.DISABLED, style="TButton")  # Применяем стиль
        self.edit_button.pack(side=tk.LEFT, padx=2)

        self.delete_button = ttk.Button(self.buttons_frame, text="Удалить", command=self.delete_customer, state=tk.DISABLED, style="TButton")  # Применяем стиль
        self.delete_button.pack(side=tk.LEFT, padx=2)

    # ... (остальной код CustomerFrame) ...

    def load_customers(self, customers=None):  # Добавили необязательный параметр
        """Загружает список клиентов из базы данных и отображает в Treeview."""
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)

        if customers is None:
            customers = database.get_customers()  # Используем get_customers() если customers не передан
        for customer in customers:
            self.customer_tree.insert("", tk.END, values=(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6], customer[7], customer[8], customer[9], customer[10]))  # отображение 11 колонок

    def add_customer(self):
        """Открывает диалоговое окно для добавления нового клиента."""
        if self.parent.current_user:  # Check if user is logged in
            AddCustomerDialog(self)
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")

    def edit_customer(self):
        """Открывает диалоговое окно для редактирования информации о клиенте."""
        if self.parent.current_user:  # Check if user is logged in
            if self.selected_customer_id:
                customer = database.get_customer(self.selected_customer_id) #  Получаем данные клиента
                if customer:
                    EditCustomerDialog(self, customer)
                    self.load_customers()
                else:
                    messagebox.showerror("Ошибка", "Не удалось загрузить данные клиента.")
            else:
                messagebox.showinfo("Внимание", "Выберите клиента для редактирования.")
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")

    def delete_customer(self):
        """Удаляет выбранного клиента из базы данных."""
        if self.parent.current_user: # Check if user is logged in
            if self.selected_customer_id:
                if messagebox.askyesno("Удаление клиента", "Вы уверены, что хотите удалить этого клиента?", parent=self):
                    database.delete_customer(self.selected_customer_id)
                    self.load_customers() # Обновляем список
                    self.edit_button["state"] = tk.DISABLED
                    self.delete_button["state"] = tk.DISABLED
                    self.selected_customer_id = None # Сбрасываем ID
            else:
                messagebox.showinfo("Внимание", "Выберите клиента для удаления.", parent=self)
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")

    def on_customer_select(self, event):
        """Обрабатывает выбор клиента в Treeview."""
        try:
            selected_item = self.customer_tree.selection()[0]
            self.selected_customer_id = self.customer_tree.item(selected_item)['values'][0]
            self.edit_button["state"] = tk.NORMAL #  Включаем кнопки
            self.delete_button["state"] = tk.NORMAL
        except IndexError:
            self.selected_customer_id = None
            self.edit_button["state"] = tk.DISABLED
            self.delete_button["state"] = tk.DISABLED

    def apply_filter(self, event=None):  # Добавлено event=None для обработки события
        """Применяет фильтр по типу клиента."""
        customer_type = self.customer_type_str.get()
        filtered_customers = database.get_segmented_customers(customer_type)
        self.load_customers(filtered_customers)

class AddCustomerDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, title="Добавить клиента")

    def body(self, master):
        # --- Тип клиента ---
        ttk.Label(master, text="Тип клиента:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
        self.customer_type_entry = ttk.Combobox(master, values=["Физическое лицо", "Юридическое лицо"], state="readonly", style="TCombobox")  # Применяем стиль
        self.customer_type_entry.set("Физическое лицо")  # Значение по умолчанию
        self.customer_type_entry.grid(row=0, column=1, sticky=tk.E)

        # --- Имя ---
        ttk.Label(master, text="Имя:", style="TLabel").grid(row=1, column=0, sticky=tk.W)
        self.first_name_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.first_name_entry.grid(row=1, column=1, sticky=tk.E)

        # --- Фамилия ---
        ttk.Label(master, text="Фамилия:", style="TLabel").grid(row=2, column=0, sticky=tk.W)
        self.last_name_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.last_name_entry.grid(row=2, column=1, sticky=tk.E)

        # --- Компания ---
        ttk.Label(master, text="Компания:", style="TLabel").grid(row=3, column=0, sticky=tk.W)
        self.company_name_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.company_name_entry.grid(row=3, column=1, sticky=tk.E)

        # --- Контактное лицо ---
        ttk.Label(master, text="Контактное лицо:", style="TLabel").grid(row=4, column=0, sticky=tk.W)
        self.contact_name_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.contact_name_entry.grid(row=4, column=1, sticky=tk.E)

        # --- Email ---
        ttk.Label(master, text="Email:", style="TLabel").grid(row=5, column=0, sticky=tk.W)
        self.email_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.email_entry.grid(row=5, column=1, sticky=tk.E)

        # --- Телефон ---
        ttk.Label(master, text="Телефон:", style="TLabel").grid(row=6, column=0, sticky=tk.W)
        self.phone_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.phone_entry.grid(row=6, column=1, sticky=tk.E)

        # --- Адрес ---
        ttk.Label(master, text="Адрес:", style="TLabel").grid(row=7, column=0, sticky=tk.W)
        self.address_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.address_entry.grid(row=7, column=1, sticky=tk.E)

        # --- Дата регистрации ---
        ttk.Label(master, text="Дата регистрации:", style="TLabel").grid(row=8, column=0, sticky=tk.W)
        self.registration_date_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.registration_date_entry.grid(row=8, column=1, sticky=tk.E)

        # --- Заметки ---
        ttk.Label(master, text="Заметки:", style="TLabel").grid(row=9, column=0, sticky=tk.W)
        self.notes_entry = ttk.Entry(master, style="TEntry")  # Применяем стиль
        self.notes_entry.grid(row=9, column=1, sticky=tk.E)

        return self.first_name_entry  # initial focus

    def apply(self):
        customer_type = self.customer_type_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        company_name = self.company_name_entry.get()
        contact_name = self.contact_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        registration_date = self.registration_date_entry.get()
        notes = self.notes_entry.get()

        database.insert_customer(customer_type, first_name, last_name, company_name, contact_name, email, phone, address, registration_date, notes)
        self.parent.load_customers()

class EditCustomerDialog(simpledialog.Dialog):
    def __init__(self, parent, customer):
        self.parent = parent
        self.customer = customer
        super().__init__(parent, title="Редактировать клиента")

    def body(self, master):
        # --- Тип клиента ---
        ttk.Label(master, text="Тип клиента:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
        self.customer_type_entry = ttk.Combobox(master, values=["Физическое лицо", "Юридическое лицо"], state="readonly", style="TCombobox")
        self.customer_type_entry.set(self.customer[1] or "Физическое лицо")  # Значение из базы или значение по умолчанию
        self.customer_type_entry.grid(row=0, column=1, sticky=tk.E)

        # --- Имя ---
        ttk.Label(master, text="Имя:", style="TLabel").grid(row=1, column=0, sticky=tk.W)
        self.first_name_entry = ttk.Entry(master, style="TEntry")
        self.first_name_entry.insert(0, self.customer[2] or "")  #  Заполняем текущими данными
        self.first_name_entry.grid(row=1, column=1, sticky=tk.E)

        # --- Фамилия ---
        ttk.Label(master, text="Фамилия:", style="TLabel").grid(row=2, column=0, sticky=tk.W)
        self.last_name_entry = ttk.Entry(master, style="TEntry")
        self.last_name_entry.insert(0, self.customer[3] or "")
        self.last_name_entry.grid(row=2, column=1, sticky=tk.E)

        # --- Компания ---
        ttk.Label(master, text="Компания:", style="TLabel").grid(row=3, column=0, sticky=tk.W)
        self.company_name_entry = ttk.Entry(master, style="TEntry")
        self.company_name_entry.insert(0, self.customer[4] or "")
        self.company_name_entry.grid(row=3, column=1, sticky=tk.E)

        # --- Контактное лицо ---
        ttk.Label(master, text="Контактное лицо:", style="TLabel").grid(row=4, column=0, sticky=tk.W)
        self.contact_name_entry = ttk.Entry(master, style="TEntry")
        self.contact_name_entry.insert(0, self.customer[5] or "")
        self.contact_name_entry.grid(row=4, column=1, sticky=tk.E)

        # --- Email ---
        ttk.Label(master, text="Email:", style="TLabel").grid(row=5, column=0, sticky=tk.W)
        self.email_entry = ttk.Entry(master, style="TEntry")
        self.email_entry.insert(0, self.customer[6] or "")
        self.email_entry.grid(row=5, column=1, sticky=tk.E)

        # --- Телефон ---
        ttk.Label(master, text="Телефон:", style="TLabel").grid(row=6, column=0, sticky=tk.W)
        self.phone_entry = ttk.Entry(master, style="TEntry")
        self.phone_entry.insert(0, self.customer[7] or "")
        self.phone_entry.grid(row=6, column=1, sticky=tk.E)

        # --- Адрес ---
        ttk.Label(master, text="Адрес:", style="TLabel").grid(row=7, column=0, sticky=tk.W)
        self.address_entry = ttk.Entry(master, style="TEntry")
        self.address_entry.insert(0, self.customer[8] or "")
        self.address_entry.grid(row=7, column=1, sticky=tk.E)

        # --- Дата регистрации ---
        ttk.Label(master, text="Дата регистрации:", style="TLabel").grid(row=8, column=0, sticky=tk.W)
        self.registration_date_entry = ttk.Entry(master, style="TEntry")
        self.registration_date_entry.insert(0, self.customer[9] or "")
        self.registration_date_entry.grid(row=8, column=1, sticky=tk.E)

        # --- Заметки ---
        ttk.Label(master, text="Заметки:", style="TLabel").grid(row=9, column=0, sticky=tk.W)
        self.notes_entry = ttk.Entry(master, style="TEntry")
        self.notes_entry.insert(0, self.customer[10] or "")
        self.notes_entry.grid(row=9, column=1, sticky=tk.E)

        return self.first_name_entry  # initial focus

    def apply(self):
        customer_type = self.customer_type_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        company_name = self.company_name_entry.get()
        contact_name = self.contact_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        registration_date = self.registration_date_entry.get()
        notes = self.notes_entry.get()

        database.update_customer(self.customer[0], customer_type, first_name, last_name, company_name, contact_name, email, phone, address, registration_date, notes)
        self.parent.load_customers()

class OrderFrame(ttk.Frame):
    def __init__(self, parent, main_font):
        super().__init__(parent)
        self.parent = parent
        self.main_font = main_font
        self.pack(fill="both", expand=True)
        self.selected_order_id = None
        self.selected_order_item_id = None  # Для отслеживания выбранного элемента заказа
        self.create_widgets()  # Вызываем create_widgets() первым
        self.load_orders()      # Затем вызываем load_orders()

    def create_widgets(self):
        # --- PanedWindow для разделения пространства ---
        self.paned_window = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Frame для заказов ---
        self.orders_frame = ttk.Frame(self)
        self.paned_window.add(self.orders_frame, weight=7)

        # --- LabelFrame для заказов ---
        self.orders_labelframe = ttk.LabelFrame(self.orders_frame, text="Заказы", padding=5)
        self.orders_labelframe.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Кнопка "Гарантийные случаи" ---
        self.warranty_button = ttk.Button(self.orders_labelframe, text="Гарантийные случаи", command=self.open_warranty_window, style="TButton")
        self.warranty_button.pack(side=tk.LEFT, padx=2)

        # --- Фрейм для фильтров и экспорта ---
        self.filter_frame = ttk.Frame(self.orders_labelframe)
        self.filter_frame.pack(pady=5)

        # --- Метка и поле для ввода начальной даты ---
        self.start_date_label = ttk.Label(self.filter_frame, text="Начальная дата:", style="TLabel")
        self.start_date_label.pack(side="left", padx=2)
        self.start_date_str = tk.StringVar()  #  Создаем StringVar
        self.start_date_entry = ttk.Entry(self.filter_frame, textvariable=self.start_date_str, style="TEntry")  # Связываем StringVar с Entry
        self.start_date_entry.pack(side="left", padx=2)

        # --- Метка и поле для ввода конечной даты ---
        self.end_date_label = ttk.Label(self.filter_frame, text="Конечная дата:", style="TLabel")
        self.end_date_label.pack(side="left", padx=2)
        self.end_date_str = tk.StringVar()  #  Создаем StringVar
        self.end_date_entry = ttk.Entry(self.filter_frame, textvariable=self.end_date_str, style="TEntry")  # Связываем StringVar с Entry
        self.end_date_entry.pack(side="left", padx=2)

        # --- Кнопка "Фильтр" ---
        self.filter_button = ttk.Button(self.filter_frame, text="Фильтр", command=self.apply_filter, style="TButton")
        self.filter_button.pack(side="left", padx=2)

        # --- Кнопка "Экспорт" ---
        self.export_button = ttk.Button(self.filter_frame, text="Экспорт в CSV", command=self.export_to_csv, style="TButton")  # Добавляем кнопку
        self.export_button.pack(side="left", padx=2)

        # --- Метка и Combobox для выбора статуса заказа ---
        self.status_label = ttk.Label(self.filter_frame, text="Статус:", style="TLabel")
        self.status_label.pack(side="left", padx=2)
        self.status_options = ["Все", "Принят", "В обработке", "Отправлен", "Доставлен", "Завершен", "Отменен"]
        self.status_str = tk.StringVar(value="Все")
        self.status_combobox = ttk.Combobox(self.filter_frame, textvariable=self.status_str, values=self.status_options, state="readonly", style="TCombobox")  # Применяем стиль
        self.status_combobox.pack(side="left", padx=2)
        self.status_combobox.bind("<<ComboboxSelected>>", self.apply_filter) # Обработчик события

        # --- Scrollbar для горизонтальной прокрутки ---
        self.order_tree_x_scrollbar = ttk.Scrollbar(self.orders_labelframe, orient="horizontal")
        self.order_tree_x_scrollbar.pack(side="bottom", fill="x")

        # --- Treeview для отображения списка заказов ---
        self.order_tree = ttk.Treeview(self.orders_labelframe, columns=("OrderID", "CustomerID", "OrderDate", "OrderStatus", "TotalAmount", "ShippingAddress", "PaymentMethod", "DeliveryMethod", "Notes"), show="headings", xscrollcommand=self.order_tree_x_scrollbar.set)  # Добавлено xscrollcommand
        self.order_tree.heading("OrderID", text="ID")
        self.order_tree.heading("CustomerID", text="Клиент")
        self.order_tree.heading("OrderDate", text="Дата")
        self.order_tree.heading("OrderStatus", text="Статус")
        self.order_tree.heading("TotalAmount", text="Сумма")  #  Добавлено
        self.order_tree.heading("ShippingAddress", text="Адрес доставки")
        self.order_tree.heading("PaymentMethod", text="Способ оплаты")
        self.order_tree.heading("DeliveryMethod", text="Способ доставки")
        self.order_tree.heading("Notes", text="Заметки")

        # Настройка ширины столбцов
        self.order_tree.column("OrderID", width=50)
        self.order_tree.column("CustomerID", width=100)
        self.order_tree.column("OrderDate", width=150)
        self.order_tree.column("OrderStatus", width=100)
        self.order_tree.column("TotalAmount", width=100)  #  Добавлено
        self.order_tree.column("ShippingAddress", width=150)
        self.order_tree.column("PaymentMethod", width=100)
        self.order_tree.column("DeliveryMethod", width=100)
        self.order_tree.column("Notes", width=150)

        self.order_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.order_tree.bind("<<TreeviewSelect>>", self.on_order_select)

        # --- Связываем Scrollbar с Treeview ---
        self.order_tree_x_scrollbar.config(command=self.order_tree.xview)

        # --- Кнопки управления заказами ---
        self.buttons_frame = ttk.Frame(self.orders_labelframe)
        self.buttons_frame.pack(pady=5)

        self.add_button = ttk.Button(self.buttons_frame, text="Добавить", command=self.add_order, style="TButton")  # Применяем стиль
        self.add_button.pack(side=tk.LEFT, padx=2)

        self.edit_button = ttk.Button(self.buttons_frame, text="Редактировать", command=self.edit_order, state=tk.DISABLED, style="TButton") # Применяем стиль
        self.edit_button.pack(side=tk.LEFT, padx=2)

        self.delete_button = ttk.Button(self.buttons_frame, text="Удалить", command=self.delete_order, state=tk.DISABLED, style="TButton") # Применяем стиль
        self.delete_button.pack(side=tk.LEFT, padx=2)

        # --- Frame для элементов заказа ---
        self.order_items_frame = ttk.Frame(self)
        self.paned_window.add(self.order_items_frame, weight=3)

        # --- LabelFrame для элементов заказа ---
        self.order_items_labelframe = ttk.LabelFrame(self.order_items_frame, text="Элементы заказа", padding=5)
        self.order_items_labelframe.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Treeview для отображения элементов заказа ---
        self.order_item_tree = ttk.Treeview(self.order_items_labelframe, columns=("OrderItemID", "ProductID", "Quantity", "UnitPrice"), show="headings")
        self.order_item_tree.heading("OrderItemID", text="ID")
        self.order_item_tree.heading("ProductID", text="Продукт")
        self.order_item_tree.heading("Quantity", text="Количество")
        self.order_item_tree.heading("UnitPrice", text="Цена")

        # Настройка ширины столбцов
        self.order_item_tree.column("OrderItemID", width=50)
        self.order_item_tree.column("ProductID", width=100)
        self.order_item_tree.column("Quantity", width=80)
        self.order_item_tree.column("UnitPrice", width=80)

        self.order_item_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.order_item_tree.bind("<<TreeviewSelect>>", self.on_order_item_select)  # Обработчик выбора элемента заказа

        # --- Кнопки управления элементами заказа ---
        self.order_item_buttons_frame = ttk.Frame(self.order_items_labelframe)
        self.order_item_buttons_frame.pack(pady=5)

        self.add_item_button = ttk.Button(self.order_item_buttons_frame, text="Добавить элемент", command=self.add_order_item, state=tk.DISABLED, style="TButton") # Применяем стиль
        self.add_item_button.pack(side=tk.LEFT, padx=2)

        self.edit_item_button = ttk.Button(self.order_item_buttons_frame, text="Редактировать элемент", command=self.edit_order_item, state=tk.DISABLED, style="TButton")  # Применяем стиль
        self.edit_item_button.pack(side=tk.LEFT, padx=2)

        self.delete_item_button = ttk.Button(self.order_item_buttons_frame, text="Удалить элемент", command=self.delete_order_item, state=tk.DISABLED, style="TButton") # Применяем стиль
        self.delete_item_button.pack(side=tk.LEFT, padx=2)

    # ... (остальной код OrderFrame) ...

    def open_warranty_window(self):
        """Открывает окно для управления гарантийными случаями."""
        WarrantyWindow(self)

    def export_to_csv(self):
        """Экспортирует данные заказов в CSV-файл."""
        #  Получаем список заказов (с учетом фильтра)
        start_date_str = self.start_date_str.get()
        end_date_str = self.end_date_str.get()

        try:
            # Преобразуем строки в объекты datetime.date
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        # Вызываем функцию для получения отфильтрованных заказов
        orders = database.get_orders_by_date_range(start_date, end_date)

        if not orders:
            messagebox.showinfo("Информация", "Нет данных для экспорта.")
            return

        #  Открываем диалоговое окно для выбора файла
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

        if not filepath:
            return  #  Если пользователь отменил выбор файла

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)

                #  Записываем заголовки столбцов
                csv_writer.writerow(["OrderID", "CustomerID", "OrderDate", "OrderStatus", "TotalAmount", "ShippingAddress", "PaymentMethod", "DeliveryMethod", "Notes"])

                #  Записываем данные заказов
                for order in orders:
                    csv_writer.writerow(order)

            messagebox.showinfo("Информация", f"Данные успешно экспортированы в файл:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при экспорте данных:\n{e}")

    def on_date_change(self, *args):
        """Вызывается при изменении текста в полях ввода даты."""
        start_date_str = self.start_date_str.get()  #  Получаем значение из StringVar
        end_date_str = self.end_date_str.get()  #  Получаем значение из StringVar

        if not start_date_str and not end_date_str:
            # Если оба поля пустые, загружаем все заказы
            self.load_orders()
            return

        try:
            # Преобразуем строки в объекты datetime.date
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        # Вызываем функцию для получения отфильтрованных заказов
        filtered_orders = database.get_orders_by_date_range(start_date, end_date)
        self.load_orders(filtered_orders)  # Передаем отфильтрованный список в load_orders

    def apply_filter(self, event=None):
        """Применяет фильтр по дате и статусу к списку заказов."""
        start_date_str = self.start_date_str.get()  # Получаем значение из StringVar
        end_date_str = self.end_date_str.get()  # Получаем значение из StringVar
        status = self.status_str.get() # Получаем выбранный статус

        if not start_date_str and not end_date_str and status == "Все":
            # Если оба поля пустые, загружаем все заказы
            self.load_orders()
            return

        try:
            # Преобразуем строки в объекты datetime.date
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        # Фильтруем по дате
        filtered_orders = database.get_orders_by_date_range(start_date, end_date)

        # Фильтруем по статусу
        if status != "Все":
            filtered_orders = [order for order in filtered_orders if order[3] == status] # order[3] - OrderStatus

        self.load_orders(filtered_orders)  # Передаем отфильтрованный список в load_orders

    def load_orders(self, orders=None):
        """Загружает список заказов из базы данных и отображает в Treeview."""
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)

        status = self.status_str.get()  # Получаем выбранный статус
        if orders is None:
            orders = database.get_orders_by_status(status)  # Используем get_orders_by_status()

        for order in orders:
            self.order_tree.insert("", tk.END, values=(order[0], order[1], order[2], order[3], order[4], order[5], order[6], order[7], order[8]))

    def add_order(self):
        # Открывает диалоговое окно для добавления нового заказа
        if self.parent.current_user: # Check if user is logged in
            AddOrderDialog(self)
            self.load_orders() # Обновляем список заказов после добавления
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")

    def edit_order(self):
        # Открывает диалоговое окно для редактирования информации о заказе
        if self.parent.current_user: # Check if user is logged in
            if self.selected_order_id:
                order = database.get_order(self.selected_order_id)  # Получаем данные заказа
                if order:
                    EditOrderDialog(self, order)  # Открываем диалог редактирования
                    self.load_orders()  # Обновляем список заказов
                else:
                    messagebox.showerror("Ошибка", "Не удалось загрузить данные заказа.")
            else:
                messagebox.showinfo("Внимание", "Выберите заказ для редактирования.")
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")


    def delete_order(self):
        # Удаляет выбранный заказ из базы данных
        if self.parent.current_user: # Check if user is logged in
            if self.selected_order_id:
                if messagebox.askyesno("Удаление заказа", "Вы уверены, что хотите удалить этот заказ?", parent=self):
                    database.delete_order(self.selected_order_id)
                    self.load_orders()  # Обновляем список заказов
                    self.clear_order_items() #Очищаем элементы заказа
                    self.edit_button["state"] = tk.DISABLED  # Отключаем кнопки
                    self.delete_button["state"] = tk.DISABLED
                    self.add_item_button["state"] = tk.DISABLED
                    self.selected_order_id = None  # Сбрасываем ID
            else:
                messagebox.showinfo("Внимание", "Выберите заказ для удаления.", parent=self)
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")


    def on_order_select(self, event):
        # Обрабатывает выбор заказа в Treeview
        try:
            selected_item = self.order_tree.selection()[0]
            self.selected_order_id = self.order_tree.item(selected_item)['values'][0]
            self.edit_button["state"] = tk.NORMAL
            self.delete_button["state"] = tk.NORMAL
            self.add_item_button["state"] = tk.NORMAL  # Включаем кнопку "Добавить элемент"
            self.load_order_items() #Загружаем элементы заказа
        except IndexError:
            self.selected_order_id = None            
            self.edit_button["state"] = tk.DISABLED
            self.delete_button["state"] = tk.DISABLED
            self.add_item_button["state"] = tk.DISABLED
            self.clear_order_items()

    def load_order_items(self, selected_order_item_id=None):
        # Загружает элементы заказа в Treeview
        for item in self.order_item_tree.get_children():
            self.order_item_tree.delete(item)

        total_amount = 0  # Инициализируем общую сумму

        if self.selected_order_id:
            order_items = database.get_order_items(self.selected_order_id)
            if order_items:
                for item in order_items:
                    # Получаем имя продукта по ID
                    product = database.get_product(item[1])  # item[1] - ProductID
                    if product:
                        product_name = product[0]  # Имя продукта
                    else:
                        product_name = "Неизвестный продукт"
                    self.order_item_tree.insert("", tk.END, values=(item[0], product_name, item[2], item[3]))  # item[0] - OrderItemID, product_name вместо item[1], item[2] - Quantity, item[3] - UnitPrice
                    try:
                        quantity = int(item[2])
                        unit_price = float(item[3])
                        total_amount += quantity * unit_price # Рассчитываем общую сумму
                    except (ValueError, TypeError) as e:  # Обрабатываем ошибки
                        print(f"Ошибка при расчете общей суммы: {e}")
                        continue  # Пропускаем эту итерацию

        # Обновляем информацию о заказе в Treeview
        for item in self.order_tree.get_children():
            if self.order_tree.item(item, "values")[0] == self.selected_order_id:
                values = list(self.order_tree.item(item, "values"))
                values[4] = f"{total_amount:.2f}"  # Обновляем TotalAmount
                self.order_tree.item(item, values=values)
                break

        # Устанавливаем фокус и выделение на добавленный элемент
        if selected_order_item_id:
            for item in self.order_item_tree.get_children():
                values = self.order_item_tree.item(item, "values")
                if values and values[0] == selected_order_item_id:
                    self.order_item_tree.selection_set(item)  # Выделяем строку
                    self.order_item_tree.focus(item)  # Устанавливаем фокус
                    break

        # Обновляем информацию о заказе в Treeview
        for item in self.order_tree.get_children():
            if self.order_tree.item(item, "values")[0] == self.selected_order_id:
                values = list(self.order_tree.item(item, "values"))
                values[4] = f"{total_amount:.2f}"  # Обновляем TotalAmount
                self.order_tree.item(item, values=values)
                break

        # Устанавливаем фокус и выделение на добавленный элемент
        if selected_order_item_id:
            for item in self.order_item_tree.get_children():
                values = self.order_item_tree.item(item, "values")
                if values and values[0] == selected_order_item_id:
                    self.order_item_tree.selection_set(item)  # Выделяем строку
                    self.order_item_tree.focus(item)  # Устанавливаем фокус
                    break

    def clear_order_items(self):
        # Очищает Treeview с элементами заказа
        for item in self.order_item_tree.get_children():
            self.order_item_tree.delete(item)
        self.edit_item_button["state"] = tk.DISABLED  # Отключаем кнопки
        self.delete_item_button["state"] = tk.DISABLED

    def add_order_item(self):
        # Открывает диалоговое окно для добавления нового элемента заказа
        if self.selected_order_id:
            AddOrderItemDialog(self, self.selected_order_id) #Передаем ID заказа в диалог
            self.load_order_items()  # Обновляем список элементов заказа
        else:
            messagebox.showinfo("Внимание", "Выберите заказ для добавления элементов.", parent=self)

    def edit_order_item(self):
        #Редактирует выбранный элемент заказа
        if self.selected_order_item_id:
            order_item = database.get_order_item(self.selected_order_item_id)  # Получаем данные элемента заказа
            if order_item:
                EditOrderItemDialog(self, order_item)  # Открываем диалог редактирования
                self.load_order_items()  # Обновляем список элементов заказа
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить данные элемента заказа.")
        else:
            messagebox.showinfo("Внимание", "Выберите элемент заказа для редактирования.", parent=self)

    def delete_order_item(self):
        #Удаляет выбранный элемент заказа
        if self.selected_order_item_id:
            if messagebox.askyesno("Удаление элемента заказа", "Вы уверены, что хотите удалить этот элемент заказа?", parent=self):
                database.delete_order_item(self.selected_order_item_id)
                self.load_order_items()  # Обновляем список элементов заказа
                self.edit_item_button["state"] = tk.DISABLED  # Отключаем кнопки
                self.delete_item_button["state"] = tk.DISABLED
                self.selected_order_item_id = None  # Сбрасываем ID
            else:
                messagebox.showinfo("Внимание", "Выберите элемент заказа для удаления.", parent=self)
        else:
            messagebox.showinfo("Внимание", "Выберите элемент заказа для удаления.", parent=self)

    def on_order_item_select(self, event):
        #Обрабатывает выбор элемента заказа в Treeview
        try:
            selected_item = self.order_item_tree.selection()[0]
            self.selected_order_item_id = self.order_item_tree.item(selected_item)['values'][0]
            self.edit_item_button["state"] = tk.NORMAL  # Включаем кнопки
            self.delete_item_button["state"] = tk.NORMAL
        except IndexError:
            self.selected_order_item_id = None
            self.edit_item_button["state"] = tk.DISABLED
            self.delete_item_button["state"] = tk.DISABLED

class WarrantyWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Гарантийные случаи")
        self.geometry("800x600")
        self.minsize(800, 600)

        self.create_widgets()

    def create_widgets(self):
        # --- Treeview для отображения списка гарантийных случаев ---
        self.warranty_tree = ttk.Treeview(self, columns=("WarrantyCaseID", "OrderID", "CustomerID", "ProductID", "CaseDate", "Description", "Status"), show="headings")
        self.warranty_tree.heading("WarrantyCaseID", text="ID")
        self.warranty_tree.heading("OrderID", text="Заказ")
        self.warranty_tree.heading("CustomerID", text="Клиент")
        self.warranty_tree.heading("ProductID", text="Продукт")
        self.warranty_tree.heading("CaseDate", text="Дата обращения")
        self.warranty_tree.heading("Description", text="Описание")
        self.warranty_tree.heading("Status", text="Статус")
        # Настройка ширины столбцов (по желанию)
        self.warranty_tree.column("WarrantyCaseID", width=50)
        self.warranty_tree.column("OrderID", width=80)
        self.warranty_tree.column("CustomerID", width=80)
        self.warranty_tree.column("ProductID", width=80)
        self.warranty_tree.column("CaseDate", width=100)
        self.warranty_tree.column("Description", width=200)
        self.warranty_tree.column("Status", width=100)
        self.warranty_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.warranty_tree.bind("<<TreeviewSelect>>", self.on_warranty_case_select)  #  Добавлено
        # --- Кнопки управления гарантийными случаями ---
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(pady=5)
        self.add_button = ttk.Button(self.buttons_frame, text="Добавить", command=self.add_warranty_case, style="TButton")
        self.add_button.pack(side=tk.LEFT, padx=2)
        self.edit_button = ttk.Button(self.buttons_frame, text="Редактировать", command=self.edit_warranty_case, state=tk.DISABLED, style="TButton")
        self.edit_button.pack(side=tk.LEFT, padx=2)
        self.delete_button = ttk.Button(self.buttons_frame, text="Удалить", command=self.delete_warranty_case, state=tk.DISABLED, style="TButton")
        self.delete_button.pack(side=tk.LEFT, padx=2)
        self.load_warranty_cases()  # Загружаем данные при создании окна

    def on_warranty_case_select(self, event):
        """Обрабатывает выбор гарантийного случая в Treeview."""
        selected_item = self.warranty_tree.selection()
        if selected_item:
            self.edit_button["state"] = tk.NORMAL  # Включаем кнопку "Редактировать"
            self.delete_button["state"] = tk.NORMAL  # Включаем кнопку "Удалить"
        else:
            self.edit_button["state"] = tk.DISABLED # Выключаем кнопку "Редактировать"
            self.delete_button["state"] = tk.DISABLED # Выключаем кнопку "Удалить"

    def load_warranty_cases(self):
        """Загружает список гарантийных случаев из базы данных и отображает в Treeview."""
        for item in self.warranty_tree.get_children():
            self.warranty_tree.delete(item)

        conn = database.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT WarrantyCaseID, OrderID, CustomerID, ProductID, CaseDate, Description, Status FROM WarrantyCases") #  Изменено
                warranty_cases = cursor.fetchall()

                for case in warranty_cases:
                    self.warranty_tree.insert("", tk.END, values=(case[0], case[1], case[2], case[3], case[4], case[5], case[6]))  # Добавлено
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()

    def add_warranty_case(self):
        """Открывает диалоговое окно для добавления нового гарантийного случая."""
        if self.parent.parent.current_user:  # Check if user is logged in
            AddWarrantyCaseDialog(self)
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")

    def edit_warranty_case(self):
        """Открывает диалоговое окно для редактирования информации о гарантийном случае."""
        if self.parent.parent.current_user:  # Check if user is logged in
            selected_item = self.warranty_tree.selection()
            if selected_item:
                warranty_case_id = self.warranty_tree.item(selected_item[0])['values'][0]
                conn = database.create_connection()
                warranty_case = None
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM WarrantyCases WHERE WarrantyCaseID = ?", (warranty_case_id,))
                        warranty_case = cursor.fetchone()
                    except sqlite3.Error as e:
                        print(e)
                    finally:
                        conn.close()
                if warranty_case:
                    EditWarrantyCaseDialog(self, warranty_case)
            else:
                messagebox.showinfo("Внимание", "Выберите гарантийный случай для редактирования.")
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")

    def delete_warranty_case(self):
        """Удаляет выбранный гарантийный случай из базы данных."""
        if self.parent.parent.current_user:  # Check if user is logged in
            selected_item = self.warranty_tree.selection()
            if selected_item:
                warranty_case_id = self.warranty_tree.item(selected_item[0])['values'][0]
                if messagebox.askyesno("Удаление гарантийного случая", "Вы уверены, что хотите удалить этот гарантийный случай?", parent=self):
                    conn = database.create_connection()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM WarrantyCases WHERE WarrantyCaseID = ?", (warranty_case_id,))
                            conn.commit()
                            print("Гарантийный случай удален.")
                        except sqlite3.Error as e:
                            print(f"Ошибка при удалении гарантийного случая: {e}")
                        finally:
                            conn.close()
                    self.load_warranty_cases()  # Обновляем список в окне
            else:
                messagebox.showinfo("Внимание", "Выберите гарантийный случай для удаления.")
        else:
            messagebox.showinfo("Внимание", "Необходимо войти в систему.")

class AddWarrantyCaseDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.parent = parent
        self.customers = database.get_customers()
        self.products = database.get_products()
        self.orders = database.get_orders()
        super().__init__(parent, title="Добавить гарантийный случай")

    def body(self, master):
        # --- ID Заказа ---
        ttk.Label(master, text="Заказ:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
        self.order_id_combobox = ttk.Combobox(master, values=[f"ID: {o[0]}" for o in self.orders], state="readonly", style="TCombobox")
        self.order_id_combobox.grid(row=0, column=1, sticky=tk.E)
        if self.orders:
            self.order_id_combobox.current(0)  # Выбор первого заказа по умолчанию

        # --- ID Клиента ---
        ttk.Label(master, text="Клиент:", style="TLabel").grid(row=1, column=0, sticky=tk.W)
        self.customer_id_combobox = ttk.Combobox(master, values=[f"{c[2]} {c[3]} ({c[0]})" for c in self.customers], state="readonly", style="TCombobox")  # Имя Фамилия (ID)
        self.customer_id_combobox.grid(row=1, column=1, sticky=tk.E)
        if self.customers:
            self.customer_id_combobox.current(0)  # Выбор первого клиента по умолчанию

        # --- ID Продукта ---
        ttk.Label(master, text="Продукт:", style="TLabel").grid(row=2, column=0, sticky=tk.W)
        self.product_id_combobox = ttk.Combobox(master, values=[p[0] for p in self.products], state="readonly", style="TCombobox")  # ProductName
        self.product_id_combobox.grid(row=2, column=1, sticky=tk.E)
        if self.products:
            self.product_id_combobox.current(0)  # Выбор первого продукта по умолчанию

        # --- Дата обращения ---
        ttk.Label(master, text="Дата обращения:", style="TLabel").grid(row=3, column=0, sticky=tk.W)
        self.case_date_entry = ttk.Entry(master, style="TEntry")
        self.case_date_entry.grid(row=3, column=1, sticky=tk.E)

        # --- Описание ---
        ttk.Label(master, text="Описание:", style="TLabel").grid(row=4, column=0, sticky=tk.W)
        self.description_entry = ttk.Entry(master, style="TEntry")
        self.description_entry.grid(row=4, column=1, sticky=tk.E)

        # --- Статус ---
        ttk.Label(master, text="Статус:", style="TLabel").grid(row=5, column=0, sticky=tk.W)
        self.status_entry = ttk.Combobox(master, values=["Принято", "В работе", "Завершено", "Отклонено"], state="readonly", style="TCombobox")
        self.status_entry.set("Принято")  # Значение по умолчанию
        self.status_entry.grid(row=5, column=1, sticky=tk.E)

        return self.order_id_combobox  # initial focus

    def apply(self):
        #  Получаем ID заказа
        selected_order_info = self.order_id_combobox.get()
        order_id = None
        if selected_order_info:
             import re
             match = re.search(r'ID: (.*)', selected_order_info)
             if match:
                  try:
                       order_id = int(match.group(1))
                  except ValueError:
                       messagebox.showerror("Ошибка", "Неверный формат ID заказа.")
                       return

        # Получаем ID клиента
        selected_customer_info = self.customer_id_combobox.get()
        customer_id = None
        if selected_customer_info:
            # Извлекаем ID клиента из строки (Имя Фамилия (ID))
            import re
            match = re.search(r'\((.*?)\)', selected_customer_info)
            if match:
                try:
                    customer_id = int(match.group(1))
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат ID клиента.")
                    return

        # Получаем ID продукта
        selected_product_name = self.product_id_combobox.get()
        product_id = None
        if selected_product_name:
            for product in self.products:
                if product[0] == selected_product_name:
                    product_id = product[1]
                    break

        case_date = self.case_date_entry.get()
        description = self.description_entry.get()
        status = self.status_entry.get()

        if order_id is None or customer_id is None or product_id is None:
            messagebox.showerror("Ошибка", "Заполните все поля.")
            return

        # Добавляем гарантийный случай в базу данных
        conn = database.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO WarrantyCases (OrderID, CustomerID, ProductID, CaseDate, Description, Status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (order_id, customer_id, product_id, case_date, description, status)) # Добавлено
                conn.commit()
                print("Гарантийный случай добавлен.")
            except sqlite3.Error as e:
                print(f"Ошибка при добавлении гарантийного случая: {e}")
            finally:
                conn.close()

        self.parent.load_warranty_cases()

class EditWarrantyCaseDialog(simpledialog.Dialog):
    def __init__(self, parent, warranty_case):
        self.parent = parent
        self.warranty_case = warranty_case
        self.customers = database.get_customers()
        self.products = database.get_products()
        self.orders = database.get_orders()
        super().__init__(parent, title="Редактировать гарантийный случай")

    def body(self, master):
        # --- ID Заказа ---
        ttk.Label(master, text="Заказ:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
        self.order_id_combobox = ttk.Combobox(master, values=[f"ID: {o[0]}" for o in self.orders], state="readonly", style="TCombobox")
        self.order_id_combobox.grid(row=0, column=1, sticky=tk.E)
        current_order_id = self.warranty_case[1]  # OrderID
        self.order_id_combobox.set(f"ID: {current_order_id}")  # Устанавливаем текущий OrderID

        # --- ID Клиента ---
        ttk.Label(master, text="Клиент:", style="TLabel").grid(row=1, column=0, sticky=tk.W)
        self.customer_id_combobox = ttk.Combobox(master, values=[f"{c[2]} {c[3]} ({c[0]})" for c in self.customers], state="readonly", style="TCombobox")  # Имя Фамилия (ID)
        self.customer_id_combobox.grid(row=1, column=1, sticky=tk.E)
        current_customer_id = self.warranty_case[2]  # CustomerID
        current_customer = next((c for c in self.customers if c[0] == current_customer_id), None)
        if current_customer:
            self.customer_id_combobox.set(f"{current_customer[2]} {current_customer[3]} ({current_customer[0]})")  # Устанавливаем текущий CustomerID

        # --- ID Продукта ---
        ttk.Label(master, text="Продукт:", style="TLabel").grid(row=2, column=0, sticky=tk.W)
        self.product_id_combobox = ttk.Combobox(master, values=[p[0] for p in self.products], state="readonly", style="TCombobox")  # ProductName
        self.product_id_combobox.grid(row=2, column=1, sticky=tk.E)
        current_product_id = self.warranty_case[3]  # ProductID
        current_product = next((p for p in self.products if p[1] == current_product_id), None)
        if current_product:
            self.product_id_combobox.set(current_product[0])  # Устанавливаем текущий ProductID

        # --- Дата обращения ---
        ttk.Label(master, text="Дата обращения:", style="TLabel").grid(row=3, column=0, sticky=tk.W)
        self.case_date_entry = ttk.Entry(master, style="TEntry")
        self.case_date_entry.insert(0, self.warranty_case[4] or "")  # CaseDate
        self.case_date_entry.grid(row=3, column=1, sticky=tk.E)

        # --- Описание ---
        ttk.Label(master, text="Описание:", style="TLabel").grid(row=4, column=0, sticky=tk.W)
        self.description_entry = ttk.Entry(master, style="TEntry")
        self.description_entry.insert(0, self.warranty_case[5] or "")  # Description
        self.description_entry.grid(row=4, column=1, sticky=tk.E)

        # --- Статус ---
        ttk.Label(master, text="Статус:", style="TLabel").grid(row=5, column=0, sticky=tk.W)
        self.status_entry = ttk.Combobox(master, values=["Принято", "В работе", "Завершено", "Отклонено"], state="readonly", style="TCombobox")
        self.status_entry.set(self.warranty_case[6] or "Принято")  # Status
        self.status_entry.grid(row=5, column=1, sticky=tk.E)

        return self.order_id_combobox  # initial focus

    def apply(self):
        #  Получаем ID заказа
        selected_order_info = self.order_id_combobox.get()
        order_id = None
        if selected_order_info:
            import re
            match = re.search(r'ID: (.*)', selected_order_info)
            if match:
                try:
                    order_id = int(match.group(1))
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат ID заказа.")
                    return

        # Получаем ID клиента
        selected_customer_info = self.customer_id_combobox.get()
        customer_id = None
        if selected_customer_info:
            # Извлекаем ID клиента из строки (Имя Фамилия (ID))
            import re
            match = re.search(r'\((.*?)\)', selected_customer_info)
            if match:
                try:
                    customer_id = int(match.group(1))
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат ID клиента.")
                    return

        # Получаем ID продукта
        selected_product_name = self.product_id_combobox.get()
        product_id = None
        if selected_product_name:
            for product in self.products:
                if product[0] == selected_product_name:
                    product_id = product[1]
                    break

        case_date = self.case_date_entry.get()
        description = self.description_entry.get()
        status = self.status_entry.get()
        warranty_case_id = self.warranty_case[0]

        database.update_warranty_case(
            warranty_case_id,
            order_id,
            customer_id,
            product_id,
            case_date,
            description,
            status
        )
        self.parent.load_warranty_cases()

class EditOrderDialog(simpledialog.Dialog):
    def __init__(self, parent, order):
        self.parent = parent
        self.order = order
        self.customers = database.get_customers()  # Получаем список клиентов
        super().__init__(parent, title="Редактировать заказ")

    def body(self, master):
        ttk.Label(master, text="Клиент:").grid(row=0, column=0, sticky=tk.W)
        # Изменяем на combobox
        self.customer_id_combobox = ttk.Combobox(master, values=[f"{c[2]} {c[3]} ({c[0]})" for c in self.customers], state="readonly")  # Отображаем имя и фамилию + ID
        self.customer_id_combobox.grid(row=0, column=1, sticky=tk.E)
        # Устанавливаем текущее значение
        current_customer_id = self.order[1]
        current_customer = next((c for c in self.customers if c[0] == current_customer_id), None)
        if current_customer:
            self.customer_id_combobox.set(f"{current_customer[2]} {current_customer[3]} ({current_customer[0]})")

        ttk.Label(master, text="Дата заказа:").grid(row=1, column=0, sticky=tk.W)
        self.order_date_entry = tk.Entry(master)
        self.order_date_entry.insert(0, self.order[2] or "")
        self.order_date_entry.grid(row=1, column=1, sticky=tk.E)

        ttk.Label(master, text="Статус заказа:").grid(row=2, column=0, sticky=tk.W)
        self.order_status_entry = ttk.Combobox(master, values=["Принят", "В обработке", "Отправлен", "Доставлен", "Завершен", "Отменен"], state="readonly")
        self.order_status_entry.set(self.order[3] or "Принят")
        self.order_status_entry.grid(row=2, column=1, sticky=tk.E)

        tk.Label(master, text="Сумма заказа:").grid(row=3, column=0, sticky=tk.W)
        self.total_amount_entry = tk.Entry(master)
        self.total_amount_entry.insert(0, self.order[4] or "")
        self.total_amount_entry.grid(row=3, column=1, sticky=tk.E)

        tk.Label(master, text="Адрес доставки:").grid(row=4, column=0, sticky=tk.W)
        self.shipping_address_entry = tk.Entry(master)
        self.shipping_address_entry.insert(0, self.order[5] or "")
        self.shipping_address_entry.grid(row=4, column=1, sticky=tk.E)

        tk.Label(master, text="Способ оплаты:").grid(row=5, column=0, sticky=tk.W)
        self.payment_method_entry = tk.Entry(master)
        self.payment_method_entry.insert(0, self.order[6] or "")
        self.payment_method_entry.grid(row=5, column=1, sticky=tk.E)

        tk.Label(master, text="Способ доставки:").grid(row=6, column=0, sticky=tk.W)
        self.delivery_method_entry = tk.Entry(master)
        self.delivery_method_entry.insert(0, self.order[7] or "")
        self.delivery_method_entry.grid(row=6, column=1, sticky=tk.E)

        tk.Label(master, text="Заметки:").grid(row=7, column=0, sticky=tk.W)
        self.notes_entry = tk.Entry(master)
        self.notes_entry.insert(0, self.order[8] or "")
        self.notes_entry.grid(row=7, column=1, sticky=tk.E)

        return self.customer_id_combobox # initial focus

    def apply(self):
        # Получаем выбранного клиента
        selected_customer_info = self.customer_id_combobox.get()
        customer_id = None
        if selected_customer_info:
            # Извлекаем ID клиента из строки (Имя Фамилия (ID))
            import re
            match = re.search(r'\((.*?)\)', selected_customer_info)
            if match:
                try:
                    customer_id = int(match.group(1))
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат ID клиента.")
                    return

        order_date = self.order_date_entry.get()
        order_status = self.order_status_entry.get()
        shipping_address = self.shipping_address_entry.get()
        payment_method = self.payment_method_entry.get()
        delivery_method = self.delivery_method_entry.get()
        notes = self.notes_entry.get()

        if customer_id is None:
            messagebox.showerror("Ошибка", "Выберите клиента.")
            return

        # Получаем все элементы заказа
        order_items = database.get_order_items(self.order[0])
        total_amount = 0
        for item in order_items:
            try:
                quantity = int(item[2])
                unit_price = float(item[3])
                total_amount += quantity * unit_price
            except (ValueError, TypeError):
                messagebox.showerror("Ошибка", "Неверный формат данных в элементах заказа.")
                return

        # Обновляем данные в базе данных
        database.update_order(self.order[0], customer_id, order_date, order_status, f"{total_amount:.2f}", shipping_address, payment_method, delivery_method, notes)
        self.parent.load_orders()

class AddOrderDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.parent = parent
        self.customers = database.get_customers() # Получаем список клиентов
        super().__init__(parent, title="Добавить заказ")

    def body(self, master):
        ttk.Label(master, text="Клиент:").grid(row=0, column=0, sticky=tk.W)
        # Изменяем на combobox
        self.customer_id_combobox = ttk.Combobox(master, values=[f"{c[2]} {c[3]} ({c[0]})" for c in self.customers], state="readonly")  # Отображаем имя и фамилию + ID
        self.customer_id_combobox.grid(row=0, column=1, sticky=tk.E)
        if self.customers:
            self.customer_id_combobox.current(0) # Выбор первого клиента по умолчанию

        ttk.Label(master, text="Дата заказа:").grid(row=1, column=0, sticky=tk.W)
        self.order_date_entry = tk.Entry(master)
        self.order_date_entry.grid(row=1, column=1, sticky=tk.E)

        ttk.Label(master, text="Статус заказа:").grid(row=2, column=0, sticky=tk.W)
        self.order_status_entry = ttk.Combobox(master, values=["Принят", "В обработке", "Отправлен", "Доставлен", "Завершен", "Отменен"], state="readonly")
        self.order_status_entry.set("Принят")  # Значение по умолчанию
        self.order_status_entry.grid(row=2, column=1, sticky=tk.E)

        ttk.Label(master, text="Сумма заказа:").grid(row=3, column=0, sticky=tk.W)
        self.total_amount_entry = tk.Entry(master)
        self.total_amount_entry.grid(row=3, column=1, sticky=tk.E)

        ttk.Label(master, text="Адрес доставки:").grid(row=4, column=0, sticky=tk.W)
        self.shipping_address_entry = tk.Entry(master)
        self.shipping_address_entry.grid(row=4, column=1, sticky=tk.E)

        ttk.Label(master, text="Способ оплаты:").grid(row=5, column=0, sticky=tk.W)
        self.payment_method_entry = tk.Entry(master)
        self.payment_method_entry.grid(row=5, column=1, sticky=tk.E)

        ttk.Label(master, text="Способ доставки:").grid(row=6, column=0, sticky=tk.W)
        self.delivery_method_entry = tk.Entry(master)
        self.delivery_method_entry.grid(row=6, column=1, sticky=tk.E)

        ttk.Label(master, text="Заметки:").grid(row=7, column=0, sticky=tk.W)
        self.notes_entry = tk.Entry(master)
        self.notes_entry.grid(row=7, column=1, sticky=tk.E)

        return self.customer_id_combobox # initial focus

    def apply(self):
        # Получаем выбранного клиента
        selected_customer_info = self.customer_id_combobox.get()
        customer_id = None
        if selected_customer_info:
            # Извлекаем ID клиента из строки (Имя Фамилия (ID))
            import re
            match = re.search(r'\((.*?)\)', selected_customer_info)
            if match:
                try:
                    customer_id = int(match.group(1))
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат ID клиента.")
                    return

        order_date = self.order_date_entry.get()
        order_status = self.order_status_entry.get()
        total_amount = self.total_amount_entry.get()
        shipping_address = self.shipping_address_entry.get()
        payment_method = self.payment_method_entry.get()
        delivery_method = self.delivery_method_entry.get()
        notes = self.notes_entry.get()

        if customer_id is None:
            messagebox.showerror("Ошибка", "Выберите клиента.")
            return

        database.insert_order(customer_id, order_date, order_status, total_amount, shipping_address, payment_method, delivery_method, notes)
        self.parent.load_orders()
        
class AddOrderItemDialog(simpledialog.Dialog):
    def __init__(self, parent, order_id):
        self.parent = parent
        self.order_id = order_id
        self.products = database.get_products()  # Получаем список продуктов
        super().__init__(parent, title="Добавить элемент заказа")

    def body(self, master):
        ttk.Label(master, text="Продукт:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
        self.product_id_combobox = ttk.Combobox(master, values=[p[0] for p in self.products], state="readonly", style="TCombobox")  # Отображаем только имена продуктов
        self.product_id_combobox.grid(row=0, column=1, sticky=tk.E)
        if self.products:
            self.product_id_combobox.current(0) # Выбираем первый элемент по умолчанию

        ttk.Label(master, text="Количество:", style="TLabel").grid(row=1, column=0, sticky=tk.W)
        self.quantity_entry = ttk.Entry(master, style="TEntry")
        self.quantity_entry.grid(row=1, column=1, sticky=tk.E)

        ttk.Label(master, text="Цена:", style="TLabel").grid(row=2, column=0, sticky=tk.W)
        self.unit_price_entry = ttk.Entry(master, style="TEntry")
        self.unit_price_entry.grid(row=2, column=1, sticky=tk.E)

        return self.product_id_combobox  # initial focus

    def apply(self):
        selected_product_name = self.product_id_combobox.get()
        product_id = None
        for p in self.products:
            if p[0] == selected_product_name:
                product_id = p[1]
                break

        if product_id is None:
            messagebox.showerror("Ошибка", "Не удалось найти ID продукта.")
            return

        try:
            quantity = int(self.quantity_entry.get())
            unit_price = float(self.unit_price_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат данных для количества и цены.")
            return

        # Добавляем элемент заказа в базу данных
        order_item_id = database.insert_order_item(self.order_id, product_id, quantity, unit_price)
        if order_item_id:
            self.parent.load_order_items(selected_order_item_id=order_item_id)  # Передаем ID нового элемента
            self.destroy()  # Закрываем диалог только при успешном добавлении

class EditOrderItemDialog(simpledialog.Dialog):
    def __init__(self, parent, order_item):
        self.parent = parent
        self.order_item = order_item
        self.products = database.get_products()  # Получаем список продуктов
        super().__init__(parent, title="Редактировать элемент заказа")

    def body(self, master):
        print(f"EditOrderItemDialog: order_item = {self.order_item}")  # Добавлено
        print(f"EditOrderItemDialog: products = {self.products}")  # Добавлено

        ttk.Label(master, text="Продукт:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
        product_names = [p[0] for p in self.products]  # Получаем список имен продуктов
        self.product_id_combobox = ttk.Combobox(master, values=product_names, state="readonly", style="TCombobox")  # Отображаем только имена продуктов
        self.product_id_combobox.grid(row=0, column=1, sticky=tk.E)

        # Выбираем текущий продукт
        current_product_name = None
        for p in self.products:
            if p[1] == self.order_item[1]:  # Сопоставляем по ID продукта
                current_product_name = p[0]
                break

        if current_product_name:
            self.product_id_combobox.set(current_product_name)

        ttk.Label(master, text="Количество:", style="TLabel").grid(row=1, column=0, sticky=tk.W)
        self.quantity_entry = ttk.Entry(master, style="TEntry")
        self.quantity_entry.insert(0, str(self.order_item[2]) or "")  # Используем item[2] для количества
        self.quantity_entry.grid(row=1, column=1, sticky=tk.E)
        print(f"Количество: {self.order_item[2]}")

        ttk.Label(master, text="Цена:", style="TLabel").grid(row=2, column=0, sticky=tk.W)
        self.unit_price_entry = ttk.Entry(master, style="TEntry")
        self.unit_price_entry.insert(0, str(self.order_item[3]) or "")  # Используем item[3] для цены
        self.unit_price_entry.grid(row=2, column=1, sticky=tk.E)
        print(f"Цена: {self.order_item[3]}")

        return self.product_id_combobox  # initial focus

    def apply(self):
        selected_product_name = self.product_id_combobox.get()
        # Находим ID продукта по выбранному имени
        product_id = None
        for name, p_id in self.products:
            if name == selected_product_name:
                product_id = p_id
                break

        if product_id is None:
            messagebox.showerror("Ошибка", "Не удалось найти ID продукта.")
            return

        try:
            quantity = int(self.quantity_entry.get())
            unit_price = float(self.unit_price_entry.get())
            order_item_id = int(self.order_item[0])

            print("Сохраняемые данные:")
            print(f"order_item_id: {order_item_id}")
            print(f"product_id: {product_id}")
            print(f"quantity: {quantity}")
            print(f"unit_price: {unit_price}")

            # Обновляем элемент заказа в базе данных
            database.update_order_item(order_item_id, product_id, quantity, unit_price)
            self.parent.load_order_items()  # Обновляем список элементов заказа
            self.parent.load_orders() #Обновляем заказы - пересчитываем сумму

        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат данных. Введите числовые значения для количества и цены.")
            return

class CustomerReportWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Отчет по клиентам")
        self.geometry("600x600")
        self.minsize(600, 600)

        self.create_widgets()
        self.load_customer_report()

    def create_widgets(self):
         # --- Фрейм для фильтров ---
        self.filter_frame = ttk.Frame(self)
        self.filter_frame.pack(pady=5)

        # --- Метка и Combobox для выбора типа клиента ---
        self.customer_type_label = ttk.Label(self.filter_frame, text="Тип клиента:")
        self.customer_type_label.pack(side="left", padx=2)
        self.customer_type_options = ["Все", "Физическое лицо", "Юридическое лицо"]
        self.customer_type_str = tk.StringVar(value="Все")
        self.customer_type_combobox = ttk.Combobox(self.filter_frame, textvariable=self.customer_type_str, values=self.customer_type_options, state="readonly")
        self.customer_type_combobox.pack(side="left", padx=2)
        self.customer_type_combobox.bind("<<ComboboxSelected>>", self.load_customer_report) #  Добавляем обработчик события

        # --- Text widget для отображения отчета ---
        self.report_text = tk.Text(self, wrap=tk.WORD)
        self.report_text.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Scrollbar для Text widget ---
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.report_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.report_text["yscrollcommand"] = self.scrollbar.set

        # --- Кнопка "Сохранить отчет" ---
        self.save_button = ttk.Button(self, text="Сохранить отчет", command=self.save_report)
        self.save_button.pack(pady=5)

    def load_customer_report(self, event=None):  # Добавляем event=None для обработки события
        """Загружает данные о клиентах из базы данных и отображает в Text widget."""
        self.report_text.delete("1.0", tk.END)  # Очищаем Text widget

        customer_type = self.customer_type_str.get()  # Получаем выбранный тип клиента

        conn = database.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if customer_type == "Все":
                    cursor.execute("SELECT * FROM Customers")
                    customers = cursor.fetchall()
                else:
                    cursor.execute("SELECT * FROM Customers WHERE CustomerType = ?", (customer_type,))
                    customers = cursor.fetchall()

                for customer in customers:
                    report_string = f"""
    ID: {customer[0]}
    Тип клиента: {customer[1]}
    Имя: {customer[2]}
    Фамилия: {customer[3]}
    Компания: {customer[4]}
    Контактное лицо: {customer[5]}
    Email: {customer[6]}
    Телефон: {customer[7]}
    Адрес: {customer[8]}
    Дата регистрации: {customer[9]}
    Заметки: {customer[10]}
    --------------------------------------
    """
                    self.report_text.insert(tk.END, report_string)
            except sqlite3.Error as e:
                print(e)
            finally:
                conn.close()

    def save_report(self):
        """Сохраняет содержимое Text widget в файл."""
        report_content = self.report_text.get("1.0", tk.END)
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(report_content)
                messagebox.showinfo("Информация", f"Отчет успешно сохранен в файл:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при сохранении файла:\n{e}")

class SalesReportWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Отчет о продажах")
        self.geometry("800x600")
        self.minsize(800, 600)

        self.create_widgets()
        self.load_sales_report()

    def create_widgets(self):
        # --- Text widget для отображения отчета ---
        self.report_text = tk.Text(self, wrap=tk.WORD)
        self.report_text.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Scrollbar для Text widget ---
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.report_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.report_text["yscrollcommand"] = self.scrollbar.set

        # --- Кнопка "Сохранить отчет" ---
        self.save_button = ttk.Button(self, text="Сохранить отчет", command=self.save_report)
        self.save_button.pack(pady=5)

    def load_sales_report(self):
        """Загружает данные о продажах из базы данных и отображает в Text widget."""
        self.report_text.delete("1.0", tk.END)  # Очищаем Text widget

        conn = database.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    SELECT
                        Orders.OrderID,
                        Orders.OrderDate,
                        Customers.CompanyName,
                        SUM(COALESCE(OrderItems.Quantity * OrderItems.UnitPrice, 0)) AS TotalAmount,
                        Customers.CustomerID
                    FROM Orders
                    INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID
                    LEFT JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
                    GROUP BY Orders.OrderID, Customers.CustomerID;
                """
                print(f"Выполняемый SQL-запрос: {sql}") # Добавлено
                cursor.execute(sql)
                sales = cursor.fetchall()

                print(f"Количество записей в отчете: {len(sales)}")

                for sale in sales:
                    print(f"Запись: {sale}")
                    report_string = f"""
        ID Заказа: {sale[0]}
        Дата: {sale[1]}
        Компания: {sale[2]}
        Сумма: {sale[3]}
        ID Клиента: {sale[4]}
        --------------------------------------
        """
                    self.report_text.insert(tk.END, report_string)
            except sqlite3.Error as e:
                print(f"Ошибка при выполнении запроса: {e}") # Добавлено
                print(e)
            finally:
                conn.close()

    def save_report(self):
        """Сохраняет содержимое Text widget в файл."""
        report_content = self.report_text.get("1.0", tk.END)
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(report_content)
                messagebox.showinfo("Информация", f"Отчет успешно сохранен в файл:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при сохранении файла:\n{e}")

class DeleteUserDialog(simpledialog.Dialog):
    def __init__(self, parent, user_names, users):
        self.parent = parent
        self.user_names = user_names
        self.users = users
        super().__init__(parent, title="Удаление пользователя")

    def body(self, master):
        #  Выпадающий список для выбора пользователя
        ttk.Label(master, text="Выберите пользователя для удаления:", style="TLabel").grid(row=0)
        self.user_combobox = ttk.Combobox(master, values=self.user_names, state="readonly", style="TCombobox")
        self.user_combobox.grid(row=0, column=1)
        if self.user_names:
            self.user_combobox.current(0)  # Выбираем первого пользователя по умолчанию

        return self.user_combobox  # initial focus

    def apply(self):
        selected_user_name = self.user_combobox.get()

        if selected_user_name:
            #  Находим пользователя по имени
            user_to_delete = next((user for user in self.users if user[1] == selected_user_name), None)
            if user_to_delete:
                #  Подтверждение удаления
                if messagebox.askyesno("Удаление пользователя", f"Вы уверены, что хотите удалить пользователя '{selected_user_name}'?", parent=self):
                    #  Удаляем пользователя из базы данных
                    database.delete_user(user_to_delete[0])  # Используем ID пользователя для удаления

                    #  Обновляем выпадающий список в форме входа (если она открыта)
                    if hasattr(self.parent, "login_dialog") and self.parent.login_dialog:
                        #  Обновляем список пользователей в LoginDialog
                        conn = database.create_connection()
                        if conn:
                            self.parent.login_dialog.users = database.get_users(conn)
                            conn.close()

                    messagebox.showinfo("Успех", f"Пользователь '{selected_user_name}' удален.")

                    #Обновляем список пользователей в текущем диалоге
                    conn = database.create_connection()
                    if conn:
                        self.users = database.get_users(conn)
                        self.user_names = [user[1] for user in self.users]
                        self.user_combobox['values'] = self.user_names
                        if self.user_names:
                            self.user_combobox.current(0)  # Выбираем первого пользователя по умолчанию
                        else:
                            self.destroy()
                            messagebox.showinfo("Внимание", "Нет пользователей для удаления.")
                        conn.close()

                else:
                    pass
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден.")
        else:
            messagebox.showerror("Ошибка", "Выберите пользователя для удаления.")

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Учет клиентов и заказов")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.current_user = None

        # --- Шрифт ---
        self.default_font = tkFont.Font(family="Helvetica", size=12)  # Инициализируем здесь

        # --- Применяем стили ---
        self.style = ttk.Style()
        configure_styles(self.style)  # Вызываем функцию настройки стилей

        # --- Добавим метку пользователя ---
        self.user_label = ttk.Label(self, text="Не авторизован", style="TLabel")
        self.user_label.pack(side=tk.TOP, anchor=tk.NE, padx=5, pady=5)  # Добавлено

        # --- Меню ---
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, font=('Helvetica', 12))
        self.file_menu.add_command(label="Зарегистрироваться", command=self.open_register_dialog)
        self.file_menu.add_command(label="Войти", command=self.open_login_dialog)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Удалить пользователя", command=self.delete_user, state=tk.DISABLED)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu, font=('Helvetica', 12))

        self.reports_menu = tk.Menu(self.menu_bar, tearoff=0, font=('Helvetica', 12))
        self.reports_menu.add_command(label="Отчет по клиентам", command=self.open_customer_report)
        self.reports_menu.add_command(label="Отчет о продажах", command=self.open_sales_report)
        self.menu_bar.add_cascade(label="Отчеты", menu=self.reports_menu)
        self.config(menu=self.menu_bar)

        self.disable_menu()  # Disable at startup

        # --- Frames ---
        self.customer_frame = CustomerFrame(self, self.default_font)
        self.order_frame = OrderFrame(self, self.default_font)
        self.current_frame = self.customer_frame  # По умолчанию отображаем CustomerFrame

        self.create_ui()
        conn = database.create_connection()
        if conn:
            try:
                database.create_tables()
                database.add_default_users(conn)
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                conn.close()
        self.update_user_label()

    def enable_menu(self):
        """Enables the menu items."""
        self.file_menu.entryconfig("Удалить пользователя", state=tk.NORMAL)

    def disable_menu(self):
        """Disables the menu items."""
        self.file_menu.entryconfig("Удалить пользователя", state=tk.DISABLED)

    def create_ui(self):
        # --- Кнопка для переключения между фреймами ---
        self.toggle_button = ttk.Button(self, text="Заказы", command=self.toggle_frame, style="TButton")
        self.toggle_button.pack(pady=5)

        # Изначально отображаем CustomerFrame
        self.customer_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.order_frame.pack_forget()  # Скрываем order frame

        # --- Настройка размеров строк и столбцов (если нужно) ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def open_register_dialog(self):
        """Opens the register dialog."""
        RegisterDialog(self)

    def open_login_dialog(self):
        """Opens the login dialog."""
        conn = database.create_connection()
        if conn:
            users = database.get_users(conn)
            self.login_dialog = LoginDialog(self, users)  # Store the dialog
            conn.close()
    def open_customer_report(self):
        """Открывает окно с отчетом по клиентам."""
        CustomerReportWindow(self)

    def open_sales_report(self):
        """Открывает окно с отчетом о продажах."""
        SalesReportWindow(self)

    def delete_user(self):
        """Удаляет выбранного пользователя."""
        if self.current_user and self.current_user[3] == "admin":
            #  Получаем список пользователей из базы данных для выпадающего списка
            conn = database.create_connection()
            if conn:
                users = database.get_users(conn)
                conn.close()
            else:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
                return

            #  Создаем диалоговое окно для выбора пользователя для удаления
            if not users:
                messagebox.showinfo("Внимание", "Нет пользователей для удаления.")
                return

            #  Создаем диалоговое окно с выпадающим списком
            user_names = [user[1] for user in users] #  Получаем список имен пользователей
            DeleteUserDialog(self, user_names, users)
        else:
            messagebox.showinfo("Внимание", "У вас нет прав для удаления пользователей.")

    def update_user_label(self):
        """Updates the user label in the main window."""
        if self.current_user:
            self.user_label.config(text=f"Пользователь: {self.current_user[1]} ({self.current_user[3]})")  # Отображение логина и роли
        else:
            self.user_label.config(text="Не авторизован")

    def toggle_frame(self):
        if self.current_frame == self.customer_frame:
            self.customer_frame.pack_forget()  # Скрываем CustomerFrame
            self.order_frame.pack(fill="both", expand=True)  # Отображаем OrderFrame
            self.current_frame = self.order_frame
            self.toggle_button.config(text="Клиенты")  # Меняем текст кнопки
        else:
            self.order_frame.pack_forget()  # Скрываем OrderFrame
            self.customer_frame.pack(fill="both", expand=True)  # Отображаем CustomerFrame
            self.current_frame = self.customer_frame
            self.toggle_button.config(text="Заказы")  # Меняем текст кнопки

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()