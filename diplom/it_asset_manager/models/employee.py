class Employee:
    def __init__(self, id=None, name=None, position=None):
        self.id = id
        self.name = name
        self.position = position # Должность сотрудника

    def __repr__(self):
        return f"Employee(id={self.id}, name='{self.name}')"