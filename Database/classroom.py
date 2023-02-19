class Classroom:
    def __init__(self, name, size, is_lab=False):
        # Name/# of Class (String)
        self.name = name
        # Student Max Capacity (Integer)
        self.size = size
        # whether the classroom is a lab (Boolean)
        self.is_lab = is_lab
        # Cohorts assigned to the Room (array of Cohorts)
        self.cohorts = []

    def add_cohort(self, cohort):
        self.cohorts.append(cohort)
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
