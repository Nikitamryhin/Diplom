import sqlite3

# Функция для создания соединения с базой данных
def create_connection():
    connection = sqlite3.connect('demo.db')
    return connection

# Функция для создания таблиц
def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Таблица Partners
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Partners(
                        id INTEGER PRIMARY KEY,
                        type TEXT NOT NULL,
                        companyname TEXT NOT NULL,
                        address TEXT NOT NULL,
                        inn INTEGER NOT NULL,
                        fiodirector TEXT NOT NULL,
                        phone INTEGER NOT NULL,
                        email TEXT NOT NULL,
                        logo BLOB NULL,
                        rating INTEGER NOT NULL,
                        marketpoint TEXT NOT NULL,
                        history INTEGER NOT NULL) ''')

    # Таблица Departments
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Departments (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL) ''')

    # Таблица Devices
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Devices (
                        id INTEGER PRIMARY KEY,
                        department_id INTEGER,
                        device_type TEXT NOT NULL,
                        model TEXT NOT NULL,
                        serial_number TEXT,
                        inventory_number TEXT,
                        cpu TEXT,
                        memory TEXT,
                        hard_drive TEXT,
                        video_card TEXT,
                        status TEXT,
                        FOREIGN KEY (department_id) REFERENCES Departments (id) ON DELETE CASCADE) ''')

    # --- Таблица Consumables ---
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Consumables (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price REAL,
                        description TEXT
                        ) ''')

    # --- Таблица DeviceConsumables ---
    cursor.execute(''' CREATE TABLE IF NOT EXISTS DeviceConsumables (
                            device_id INTEGER,
                            consumable_id INTEGER,
                            quantity INTEGER NOT NULL DEFAULT 1,
                            FOREIGN KEY (device_id) REFERENCES Devices (id) ON DELETE CASCADE,
                            FOREIGN KEY (consumable_id) REFERENCES Consumables (id) ON DELETE CASCADE,
                            PRIMARY KEY (device_id, consumable_id)
                            ) ''')

    connection.commit()
    connection.close()

# --- Функции для работы с отделами ---
def insert_department(name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Departments (name) VALUES (?)", (name,))
    connection.commit()
    department_id = cursor.lastrowid # Возвращаем id вставленной строки
    connection.close()
    return department_id # Возвращаем ID

def get_departments():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Departments")
    rows = cursor.fetchall()
    connection.close()
    return rows

def update_department(id, name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Departments SET name=? WHERE id=?", (name, id))
    connection.commit()
    connection.close()

def delete_department(id):
    connection = create_connection()
    cursor = connection.cursor()
    # Удаляем сначала связанные устройства (CASCADE будет работать из-за ON DELETE CASCADE)
    cursor.execute("DELETE FROM Devices WHERE department_id=?", (id,))
    # Затем удаляем отдел
    cursor.execute("DELETE FROM Departments WHERE id=?", (id,))
    connection.commit()
    connection.close()

# --- Функции для работы с устройствами ---
def insert_device(department_id, device_type, model, serial_number, inventory_number, cpu, memory, hard_drive, video_card, status):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Devices (department_id, device_type, model, serial_number, inventory_number, cpu, memory, hard_drive, video_card, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (department_id, device_type, model, serial_number, inventory_number, cpu, memory, hard_drive, video_card, status))
    connection.commit()
    device_id = cursor.lastrowid
    connection.close()
    return device_id

def get_devices(department_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Devices WHERE department_id=?", (department_id,))
    rows = cursor.fetchall()
    connection.close()
    return rows

def update_device(id, department_id, device_type, model, serial_number, inventory_number, cpu, memory, hard_drive, video_card, status):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Devices SET department_id=?, device_type=?, model=?, serial_number=?, inventory_number=?, cpu=?, memory=?, hard_drive=?, video_card=?, status=? WHERE id=?",
                   (department_id, device_type, model, serial_number, inventory_number, cpu, memory, hard_drive, video_card, status, id))
    connection.commit()
    connection.close()

def delete_device(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Devices WHERE id=?", (id,))
    connection.commit()
    connection.close()

# --- Функции для работы с расходными материалами ---
def insert_consumable(name, quantity, price, description):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Consumables (name, quantity, price, description) VALUES (?, ?, ?, ?)", (name, quantity, price, description))
    connection.commit()
    consumable_id = cursor.lastrowid
    connection.close()
    return consumable_id

def get_consumables():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Consumables")
    consumables = cursor.fetchall()
    connection.close()
    print(f"get_consumables() returned: {consumables}") # Добавляем print
    return consumables

def update_consumable(id, name, quantity, price, description):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Consumables SET name=?, quantity=?, price=?, description=? WHERE id=?", (name, quantity, price, description, id))
    connection.commit()
    connection.close()

def delete_consumable(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Consumables WHERE id=?", (id,))
    connection.commit()
    connection.close()

def get_consumable(id):
    connection = sqlite3.connect('demo.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Consumables WHERE id=?", (id,))
    consumable = cursor.fetchone()
    connection.close()
    return consumable

# --- Функции для работы с DeviceConsumables ---
def insert_device_consumable(device_id, consumable_id, quantity):
    connection = create_connection()
    cursor = connection.cursor()
    try: # Пытаемся вставить, если запись еще не существует
        cursor.execute("INSERT INTO DeviceConsumables (device_id, consumable_id, quantity) VALUES (?, ?, ?)", (device_id, consumable_id, quantity))
    except sqlite3.IntegrityError: # Если такая связка уже есть, обновляем количество
        cursor.execute("UPDATE DeviceConsumables SET quantity = quantity + ? WHERE device_id = ? AND consumable_id = ?", (quantity, device_id, consumable_id))

    connection.commit()
    connection.close()

def get_device_consumables(device_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(''' SELECT Consumables.id, Consumables.name, DeviceConsumables.quantity, Consumables.price, Consumables.description
                       FROM Consumables
                       INNER JOIN DeviceConsumables ON Consumables.id = DeviceConsumables.consumable_id
                       WHERE DeviceConsumables.device_id = ?''', (device_id,))
    device_consumables = cursor.fetchall()
    connection.close()
    return device_consumables

def update_device_consumable_quantity(device_id, consumable_id, quantity):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE DeviceConsumables SET quantity=? WHERE device_id=? AND consumable_id=?", (quantity, device_id, consumable_id))
    connection.commit()
    connection.close()

def delete_device_consumable(device_id, consumable_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM DeviceConsumables WHERE device_id=? AND consumable_id=?", (device_id, consumable_id))
    connection.commit()
    connection.close()


# Оставляем ваши функции для Partners (если они вам нужны):
def insert_partner(type, companyname, address, inn, fiodirector, phone, email, logo, rating, marketpoint, history):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Partners (type, companyname, address, inn, fiodirector, phone, email, logo, rating, marketpoint, history) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (type, companyname, address, inn, fiodirector, phone, email, logo, rating, marketpoint, history))
    connection.commit()
    connection.close()

def update_partner(id, type, companyname, address, inn, fiodirector, phone, email, logo, rating, marketpoint, history):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Partners SET type=?, companyname=?, address=?, inn=?, fiodirector=?, phone=?, email=?, logo=?, rating=?, marketpoint=?, history=? WHERE id=?",
                    (type, companyname, address, inn, fiodirector, phone, email, logo, rating, marketpoint, history, id))
    connection.commit()
    connection.close()

def get_partners():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Partners")
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_consumable_by_name(name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Consumables WHERE name=?", (name,))
    consumable = cursor.fetchone()
    connection.close()
    return consumable

def insert_consumable_name_only(name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Consumables (name, quantity, price, description) VALUES (?, ?, ?, ?)", (name, 0, 0.0, "")) # или значения по умолчанию
    connection.commit()
    consumable_id = cursor.lastrowid
    connection.close()
    return consumable_id

if __name__ == '__main__':
    create_tables()