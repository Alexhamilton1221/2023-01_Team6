class Classroom:
    def __init__(self, name, size, is_lab=False):
        # Name/# of Class
        self.name = name
        # Student Max Capacity
        self.size = size
        # whether the classroom is a lab
        self.is_lab = is_lab

    def same_name(self, name):
        return self.name == name

    def same_size(self, size):
        return self.size == size

    def has_lab(self):
        return self.is_lab

    def is_equal(self, other):
        if type(other) != Classroom:
            return False
        return self.same_name(other.name) and self.same_size(other.size) and self.is_lab == other.is_lab



x = Classroom("PC0102", 24)
y = Classroom("Td0203", 24, True)
