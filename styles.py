# styles.py
from tkinter import ttk

def configure_styles(style):
    """Настраивает стили для различных элементов."""
    # --- Общие стили ---
    style.configure('.',
        font=('Helvetica', 12, 'bold'),  #  Общий жирный шрифт
        background='#f0f0f0',
        foreground='#000000'
    )

    # --- Стили для меток (Labels) ---
    style.configure('TLabel',
        padding=5,
        background='#f0f0f0',
        foreground='#000000',   #  Черный текст
        font=('Helvetica', 12, 'bold') #  Жирный шрифт для меток
    )

    # --- Стили для кнопок (Buttons) ---
    style.configure('TButton',
        padding=8,
        background='#ffffff',  # Белый фон
        foreground='#000000',  # Черный текст
        relief="groove",  #  Добавляем черную обводку (groove)
        borderwidth=1,        # Толщина обводки
        font=('Helvetica', 12, 'bold'), #  Шрифт
        focuscolor='#ffffff', #  Цвет при фокусе (чтобы обводка не менялась)
        bordercolor='black' # Цвет обводки
    )
    style.map('TButton',
        background=[('active', '#f0f0f0')],  #  Серый фон при наведении
        foreground=[('active', '#000000')]   #  Черный текст при наведении
    )

    # --- Стили для полей ввода (Entry) ---
    style.configure('TEntry',
        padding=5,
        fieldbackground='#ffffff',
        bordercolor='#cccccc',
        font=('Helvetica', 12, 'bold') #  Жирный шрифт для полей ввода
    )

    # --- Стили для Treeview ---
    style.configure('Treeview',
        background="#ffffff",
        fieldbackground="#ffffff",
        foreground="#000000",
        font=('Helvetica', 12, 'bold') #  Жирный шрифт для Treeview
    )
    style.configure('Treeview.Heading',
        background="#dddddd",
        foreground="#000000",
        font=('Helvetica', 12, 'bold')
    )

    # --- Стили для Combobox ---
    style.configure('TCombobox',
        padding=5,
        fieldbackground='#ffffff',
        arrowsize=12,
        font=('Helvetica', 12, 'bold') # Жирный шрифт для Combobox
    )