import hashlib
import sqlite3

def create_connection(db_file="demo.db"):
    """Создает соединение с базой данных SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # Включаем поддержку внешних ключей
        conn.execute("PRAGMA foreign_keys = 1")
        print("Поддержка внешних ключей включена") # Добавлено
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables():
    """Создает таблицу Users, если она не существует."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username VARCHAR(255) NOT NULL UNIQUE,
                Password VARCHAR(255) NOT NULL,
                Role VARCHAR(50) DEFAULT 'user'
            );
        """)
        conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_tables():
    """Создает таблицу Customers, если она не существует."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Customers (
                CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerType VARCHAR(50) DEFAULT 'Физическое лицо',
                FirstName VARCHAR(255),
                LastName VARCHAR(255),
                CompanyName VARCHAR(255),
                ContactName VARCHAR(255),
                Email VARCHAR(255),
                Phone VARCHAR(20),
                Address VARCHAR(255),
                RegistrationDate DATE,
                Notes TEXT
            );
        """)
        # Create Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerID INTEGER,
                OrderDate DATETIME,
                OrderStatus VARCHAR(50),
                ShippingAddress VARCHAR(255),
                TotalAmount DECIMAL(10, 2),
                PaymentMethod VARCHAR(50),
                DeliveryMethod VARCHAR(50),
                Notes TEXT,
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OrderItems (
                OrderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
                OrderID INTEGER,
                ProductID INTEGER,
                Quantity INTEGER,
                UnitPrice DECIMAL(10, 2),
                FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
                FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
                ProductName VARCHAR(255),
                CategoryID INTEGER,
                Description TEXT,
                Price DECIMAL(10, 2),
                QuantityInStock INTEGER,
                FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Categories (
                CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                CategoryName VARCHAR(255),
                Description TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS WarrantyCases (
                WarrantyCaseID INTEGER PRIMARY KEY AUTOINCREMENT,
                OrderID INTEGER,
                CustomerID INTEGER,
                ProductID INTEGER,
                CaseDate DATETIME,
                Description TEXT,
                Status VARCHAR(50),
                RepairDetails TEXT,
                CompletionDate DATETIME,
                EmployeeID INTEGER,
                Notes TEXT,
                FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
                FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username VARCHAR(255) NOT NULL UNIQUE,
                Password VARCHAR(255) NOT NULL,
                Role VARCHAR(50) DEFAULT 'user'
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def insert_customer(customer_type, first_name, last_name, company_name, contact_name, email, phone, address, registration_date, notes):
    """Вставляет нового клиента в таблицу Customers."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Customers (CustomerType, FirstName, LastName, CompanyName, ContactName, Email, Phone, Address, RegistrationDate, Notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (customer_type, first_name, last_name, company_name, contact_name, email, phone, address, registration_date, notes))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return None

def get_customers():
    """Получает список всех клиентов из таблицы Customers."""
    conn = create_connection()
    customers = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Customers")
            customers = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return customers

def get_customer(customer_id):
    """Получает информацию о клиенте по его ID."""
    conn = create_connection()
    customer = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Customers WHERE CustomerID = ?", (customer_id,))
            customer = cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return customer

def update_customer(customer_id, customer_type, first_name, last_name, company_name, contact_name, email, phone, address, registration_date, notes):
    """Обновляет информацию о клиенте в таблице Customers."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Customers
                SET CustomerType = ?, FirstName = ?, LastName = ?, CompanyName = ?, ContactName = ?,
                    Email = ?, Phone = ?, Address = ?, RegistrationDate = ?, Notes = ?
                WHERE CustomerID = ?
            """, (customer_type, first_name, last_name, company_name, contact_name, email, phone, address, registration_date, notes, customer_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def delete_customer(customer_id):
    """Удаляет клиента из таблицы Customers."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Customers WHERE CustomerID = ?", (customer_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


# --- Functions for Orders ---
def insert_order(customer_id, order_date, order_status, total_amount, shipping_address="", payment_method="", delivery_method="", notes=""):
    """Вставляет новый заказ в таблицу Orders."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            print(f"Данные для вставки: CustomerID={customer_id}, OrderDate={order_date}, OrderStatus={order_status}, TotalAmount={total_amount}, ShippingAddress={shipping_address}, PaymentMethod={payment_method}, DeliveryMethod={delivery_method}, Notes={notes}")

            cursor.execute("""
                INSERT INTO Orders (CustomerID, OrderDate, OrderStatus, TotalAmount, ShippingAddress, PaymentMethod, DeliveryMethod, Notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (customer_id, order_date, order_status, total_amount, shipping_address, payment_method, delivery_method, notes))
            conn.commit()
            order_id = cursor.lastrowid
            print(f"Заказ успешно добавлен. OrderID = {order_id}")
            return order_id
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении заказа: {e}")
            return None
        finally:
            conn.close()
    return None

def get_orders():
    """Получает список всех заказов из таблицы Orders."""
    conn = create_connection()
    orders = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Orders")
            orders = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении списка заказов: {e}") #  Добавлено
        finally:
            conn.close()
    return orders

def get_order(order_id):
    """Получает информацию о заказе по его ID."""
    conn = create_connection()
    order = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Orders WHERE OrderID = ?", (order_id,))
            order = cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return order

def update_order(order_id, customer_id, order_date, order_status, total_amount, shipping_address, payment_method, delivery_method, notes):
    """Обновляет информацию о заказе."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Orders
                SET CustomerID = ?, OrderDate = ?, OrderStatus = ?, TotalAmount = ?, ShippingAddress = ?, PaymentMethod = ?, DeliveryMethod = ?, Notes = ?
                WHERE OrderID = ?
            """, (customer_id, order_date, order_status, total_amount, shipping_address, payment_method, delivery_method, notes, order_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def delete_order(order_id):
    """Удаляет заказ из таблицы Orders."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Удаляем связанные элементы заказа
            cursor.execute("DELETE FROM OrderItems WHERE OrderID = ?", (order_id,))

            # Удаляем связанные гарантийные случаи
            cursor.execute("DELETE FROM WarrantyCases WHERE OrderID = ?", (order_id,))

            # Удаляем сам заказ
            cursor.execute("DELETE FROM Orders WHERE OrderID = ?", (order_id,))

            conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при удалении заказа: {e}")
        finally:
            conn.close()

def insert_order_item(order_id, product_id, quantity, unit_price):
    """Вставляет новый элемент заказа в таблицу OrderItems."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
                VALUES (?, ?, ?, ?)
            """, (order_id, product_id, quantity, unit_price))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return None

def get_order_items(order_id):
    """Получает список элементов заказа для заданного OrderID."""
    conn = create_connection()
    order_items = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT OrderItemID, ProductID, Quantity, UnitPrice FROM OrderItems WHERE OrderID = ?", (order_id,))
            order_items = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении элементов заказа: {e}")
        finally:
            conn.close()
    return order_items

def get_order_item(order_item_id):
    """Получает информацию об элементе заказа по его ID."""
    conn = create_connection()
    order_item = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT OrderItemID, ProductID, Quantity, UnitPrice FROM OrderItems WHERE OrderItemID = ?", (order_item_id,))
            row = cursor.fetchone()
            if row:
                order_item = (row[0], row[1], row[2], row[3])
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return order_item

def update_order_item(order_item_id, product_id, quantity, unit_price):
    """Обновляет информацию о элементе заказа в таблице OrderItems."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            print(f"Обновление элемента заказа: OrderItemID={order_item_id}, ProductID={product_id}, Quantity={quantity}, UnitPrice={unit_price}")
            cursor.execute("""
                UPDATE OrderItems
                SET ProductID = ?, Quantity = ?, UnitPrice = ?
                WHERE OrderItemID = ?
            """, (product_id, quantity, unit_price, order_item_id))
            conn.commit()
            print("Обновление выполнено успешно.")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def delete_order_item(order_item_id):
    """Удаляет элемент заказа из таблицы OrderItems."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM OrderItems WHERE OrderItemID = ?", (order_item_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def get_products():
    """Получает список всех продуктов из таблицы Products."""
    conn = create_connection()
    products = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT ProductName, ProductID FROM Products")
            
            # Fetch all distinct product names with their corresponding ProductIDs
            product_names = cursor.fetchall()

            # Create a dictionary to store unique product names and their associated ProductIDs
            unique_products = {}
            for name, product_id in product_names:
                 if name not in unique_products:
                      unique_products[name] = product_id
                    
            products = [(name, product_id) for name, product_id in unique_products.items()]

            print(f"Список продуктов: {products}")

        except sqlite3.Error as e:
            print(f"Ошибка при получении списка продуктов: {e}")
        finally:
            conn.close()
    return products

def get_product(product_id):
    """Получает информацию о продукте по его ID."""
    conn = create_connection()
    product = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ProductID, ProductName FROM Products WHERE ProductID = ?", (product_id,))
            product = cursor.fetchone()
            print(f"Информация о продукте с ID {product_id}: {product}")  # Добавлено
        except sqlite3.Error as e:
            print(f"Ошибка при получении информации о продукте: {e}")
        finally:
            conn.close()
    return product

def get_orders_by_date_range(start_date, end_date):
    """Получает список заказов, созданных в заданном диапазоне дат."""
    conn = create_connection()
    orders = []
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                SELECT * FROM Orders
                WHERE 1=1
            """
            params = []

            if start_date:
                sql += " AND OrderDate >= ?"
                params.append(start_date)
            if end_date:
                sql += " AND OrderDate <= ?"
                params.append(end_date)

            cursor.execute(sql, params)
            orders = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return orders

def get_segmented_customers(customer_type):
    """Получает список клиентов с учетом фильтров по типу."""
    conn = create_connection()
    customers = []
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                SELECT * FROM Customers
                WHERE 1=1
            """
            params = []

            if customer_type != "Все":
                sql += " AND CustomerType = ?"
                params.append(customer_type)

            cursor.execute(sql, params)
            customers = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return customers

def get_segmented_customers(customer_type):
    """Получает список клиентов с учетом фильтров по типу."""
    conn = create_connection()
    customers = []
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                SELECT * FROM Customers
                WHERE 1=1
            """
            params = []

            if customer_type != "Все":
                sql += " AND CustomerType = ?"
                params.append(customer_type)

            cursor.execute(sql, params)
            customers = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return customers

def get_orders_by_status(status):
    """Получает список заказов, отфильтрованных по статусу."""
    conn = create_connection()
    orders = []
    if conn:
        try:
            cursor = conn.cursor()
            if status == "Все":
                cursor.execute("SELECT * FROM Orders")
            else:
                cursor.execute("SELECT * FROM Orders WHERE OrderStatus = ?", (status,))
            orders = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return orders

def insert_warranty_case(order_id, customer_id, product_id, case_date, description, status):
    """Вставляет новый гарантийный случай в таблицу WarrantyCases."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO WarrantyCases (OrderID, CustomerID, ProductID, CaseDate, Description, Status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (order_id, customer_id, product_id, case_date, description, status))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return None

def update_warranty_case(warranty_case_id, order_id, customer_id, product_id, case_date, description, status):
    """Обновляет информацию о гарантийном случае в таблице WarrantyCases."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE WarrantyCases
                SET OrderID = ?, CustomerID = ?, ProductID = ?, CaseDate = ?, Description = ?, Status = ?
                WHERE WarrantyCaseID = ?
            """, (order_id, customer_id, product_id, case_date, description, status, warranty_case_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def hash_password(password):
    """Hashes the password using SHA256."""
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

def insert_user(username, password, role="user"):
    """Вставляет нового пользователя в таблицу Users."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Users (Username, Password, Role)
                VALUES (?, ?, ?)
            """, (username, password, role))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return None

def get_user(username):
    """Получает информацию о пользователе по логину."""
    conn = create_connection()
    user = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
            user = cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return user

def get_users(conn):
    """Получает всех пользователей из таблицы Users."""
    users = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users")
            users = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            return users

def verify_password(password, hashed_password):
    """Verifies the password against the hashed password."""
    hashed_password_to_verify = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password == hashed_password_to_verify

def add_default_users(conn):
    """Adds default users if they don't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users")
        if cursor.fetchone()[0] == 0:
            # Хэшируем пароли
            admin_password = hash_password("admin")
            user_password = hash_password("user")
            # Добавляем пользователей
            cursor.execute("""
                INSERT INTO Users (Username, Password, Role) VALUES
                ('admin', ?, 'admin'),
                ('user', ?, 'user')
            """, (admin_password, user_password))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding default users: {e}")

def add_default_users(conn):
    """Adds default users if they don't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users")
        if cursor.fetchone()[0] == 0:
            # Хэшируем пароли
            admin_password = hash_password("admin")
            user_password = hash_password("user")
            # Добавляем пользователей
            cursor.execute("""
                INSERT INTO Users (Username, Password, Role) VALUES
                ('admin', ?, 'admin'),
                ('user', ?, 'user')
            """, (admin_password, user_password))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding default users: {e}")

def delete_user(user_id):
    """Удаляет пользователя из таблицы Users."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()
    return False