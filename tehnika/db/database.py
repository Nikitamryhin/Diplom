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
                        history TEXT NOT NULL) ''')

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

    # --- Таблица Peripherals ---
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Peripherals (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        type TEXT,           -- Тип (мышь, клавиатура, принтер и т.д.)
                        interface TEXT,      -- Интерфейс (USB, Bluetooth и т.д.)
                        manufacturer TEXT,   -- Производитель
                        resolution TEXT,     -- Разрешение (для мыши)
                        print_type TEXT,     -- Тип печати (для принтера)
                        print_speed INTEGER,  -- Скорость печати (для принтера)
                        quantity INTEGER NOT NULL,
                        price REAL,
                        description TEXT
                        ) ''')

    # --- Таблица DevicePeripherals ---
    cursor.execute(''' CREATE TABLE IF NOT EXISTS DevicePeripherals (
                            device_id INTEGER,
                            peripheral_id INTEGER,
                            quantity INTEGER NOT NULL DEFAULT 1,
                            FOREIGN KEY (device_id) REFERENCES Devices (id) ON DELETE CASCADE,
                            FOREIGN KEY (peripheral_id) REFERENCES Peripherals (id) ON DELETE CASCADE,
                            PRIMARY KEY (device_id, peripheral_id)
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

# --- Функции для работы с периферией ---
def insert_peripheral(name, type, interface, manufacturer, resolution, print_type, print_speed, quantity, price, description):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Peripherals (name, type, interface, manufacturer, resolution, print_type, print_speed, quantity, price, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (name, type, interface, manufacturer, resolution, print_type, print_speed, quantity, price, description))
    connection.commit()
    peripheral_id = cursor.lastrowid
    connection.close()
    return peripheral_id

def get_peripherals():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Peripherals")
    peripherals = cursor.fetchall()
    connection.close()
    return peripherals

def get_peripheral(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Peripherals WHERE id=?", (id,))
    peripheral = cursor.fetchone()
    connection.close()
    return peripheral

def get_peripheral_by_name(name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Peripherals WHERE name=?", (name,))
    peripheral = cursor.fetchone()
    connection.close()
    return peripheral

def insert_peripheral_name_only(name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Peripherals (name, quantity, price, description, type, interface, manufacturer, resolution, print_type, print_speed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (name, 0, 0.0, "", "", "", "", "", "", 0)) # или значения по умолчанию
    connection.commit()
    peripheral_id = cursor.lastrowid
    connection.close()
    return peripheral_id

def get_device_peripherals(device_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(''' SELECT Peripherals.id, Peripherals.name, DevicePeripherals.quantity
                               FROM Peripherals
                               INNER JOIN DevicePeripherals ON Peripherals.id = DevicePeripherals.peripheral_id
                               WHERE DevicePeripherals.device_id = ?''', (device_id,))
    device_peripherals = cursor.fetchall()
    connection.close()
    return device_peripherals

def insert_device_peripheral(device_id, peripheral_id, quantity):
    connection = create_connection()
    cursor = connection.cursor()
    try: # Пытаемся вставить, если запись еще не существует
        cursor.execute("INSERT INTO DevicePeripherals (device_id, peripheral_id, quantity) VALUES (?, ?, ?)", (device_id, peripheral_id, quantity))
    except sqlite3.IntegrityError: # Если такая связка уже есть, обновляем количество
        cursor.execute("UPDATE DevicePeripherals SET quantity = quantity + ? WHERE device_id = ? AND peripheral_id = ?", (quantity, device_id, peripheral_id))

    connection.commit()
    connection.close()

def update_device_peripheral_quantity(device_id, peripheral_id, quantity):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE DevicePeripherals SET quantity=? WHERE device_id=? AND peripheral_id=?", (quantity, device_id, peripheral_id))
    connection.commit()
    connection.close()

def delete_device_peripheral(device_id, peripheral_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM DevicePeripherals WHERE device_id=? AND peripheral_id=?", (device_id, peripheral_id))
    connection.commit()
    connection.close()