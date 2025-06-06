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
                        type TEXT NOT NULL,
                        model TEXT NOT NULL,
                        serial_number TEXT,
                        inventory_number TEXT,
                        cpu TEXT,
                        memory TEXT,
                        hard_drive TEXT,
                        video_card TEXT,
                        status TEXT,
                        FOREIGN KEY (department_id) REFERENCES Departments (id) ON DELETE CASCADE) ''')

   # Таблица Software
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Software (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        version TEXT) ''')

    # Таблица DeviceSoftware
    cursor.execute(''' CREATE TABLE IF NOT EXISTS DeviceSoftware (
                        device_id INTEGER,
                        software_id INTEGER,
                        FOREIGN KEY (device_id) REFERENCES Devices (id) ON DELETE CASCADE,
                        FOREIGN KEY (software_id) REFERENCES Software (id) ON DELETE CASCADE,
                        PRIMARY KEY (device_id, software_id)) ''')

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

def get_devices(department_id=None):
    connection = create_connection()
    cursor = connection.cursor()
    if department_id:
        cursor.execute("SELECT * FROM Devices WHERE department_id=?", (department_id,))
    else:
        cursor.execute("SELECT * FROM Devices")
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

# db/database.py
def get_devices_by_department(department_id):
    """Получает список устройств для указанного отдела."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Devices WHERE department_id = ?", (department_id,))  # Замените "Devices" на имя вашей таблицы
    devices = cursor.fetchall()
    conn.close()
    return devices

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

def delete_peripheral(peripheral_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Peripherals WHERE id=?", (peripheral_id,))
    conn.commit()
    conn.close()

def get_software_for_device(device_id):
    """Получает список установленного ПО для устройства с заданным ID."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Software.name, Software.version
        FROM DeviceSoftware
        JOIN Software ON DeviceSoftware.software_id = Software.id
        WHERE DeviceSoftware.device_id = ?
    """, (device_id,))
    software_list = cursor.fetchall()
    conn.close()
    return software_list

def get_device(id):
    connection = sqlite3.connect('demo.db')  # Замените 'demo.db' на имя вашей базы данных
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Devices WHERE id=?", (id,))
    device = cursor.fetchone()
    connection.close()
    return device

def update_peripheral(id, name, type, interface, manufacturer, resolution, print_type, print_speed, quantity, price, description):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Peripherals
        SET name=?, type=?, interface=?, manufacturer=?, resolution=?,
            print_type=?, print_speed=?, quantity=?, price=?, description=?
        WHERE id=?
    """, (name, type, interface, manufacturer, resolution, print_type, print_speed, quantity, price, description, id))
    connection.commit()
    connection.close()

def get_software_for_peripheral(peripheral_id):
    """Получает список установленного ПО для периферии с заданным ID."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT  Software.id, Software.name, Software.version
        FROM DevicePeripherals
        JOIN Peripherals ON DevicePeripherals.peripheral_id = Peripherals.id
        JOIN Devices ON DevicePeripherals.device_id = Devices.id
        JOIN DeviceSoftware ON Devices.id = DeviceSoftware.device_id
        JOIN Software ON DeviceSoftware.software_id = Software.id
        WHERE Peripherals.id = ?
    """, (peripheral_id,))
    software_list = cursor.fetchall()
    conn.close()
    return software_list

def delete_software_from_device(device_id, software_name, software_version):
    """Удаляет выбранное ПО с выбранного устройства."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM DeviceSoftware
        WHERE device_id = ?
        AND software_id IN (SELECT id FROM Software WHERE name = ? AND version = ?)
    """, (device_id, software_name, software_version))

    conn.commit()
    conn.close()

def add_software_to_device(device_id, name, version):
    """Добавляет новое ПО к устройству."""
    conn = create_connection()
    cursor = conn.cursor()

    # Сначала проверяем, существует ли уже такое ПО
    cursor.execute("SELECT id FROM Software WHERE name=? AND version=?", (name, version))
    software = cursor.fetchone()

    if software is None:
        # Если ПО не существует, добавляем его в таблицу Software
        cursor.execute("INSERT INTO Software (name, version) VALUES (?, ?)", (name, version))
        software_id = cursor.lastrowid
    else:
        # Если ПО уже существует, получаем его ID
        software_id = software[0]

    # Связываем ПО с устройством в таблице DeviceSoftware
    try:
        cursor.execute("INSERT INTO DeviceSoftware (device_id, software_id) VALUES (?, ?)", (device_id, software_id))
    except sqlite3.IntegrityError:
        # Если связь уже существует, ничего не делаем
        pass

    conn.commit()
    conn.close()