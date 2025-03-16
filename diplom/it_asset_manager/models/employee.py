class Employee:
    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position

    def __repr__(self):
        return f"Employee(id={self.id}, name='{self.name}')"