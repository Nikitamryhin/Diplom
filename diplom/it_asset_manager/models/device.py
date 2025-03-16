class Device:
    def __init__(self, id=None, name=None, category=None, serial_number=None,
                 status=None, purchase_date=None, warranty_until=None, description=None,
                 department_id=None, employee_id=None):  # Добавлены department_id и employee_id
        self.id = id
        self.name = name
        self.category = category
        self.serial_number = serial_number
        self.status = status
        self.purchase_date = purchase_date
        self.warranty_until = warranty_until
        self.description = description
        self.department_id = department_id  # ID отдела, к которому принадлежит устройство
        self.employee_id = employee_id      # ID сотрудника, ответственного за устройство

    def __repr__(self):
        return f"Device(id={self.id}, name='{self.name}', department_id={self.department_id}, employee_id={self.employee_id})"