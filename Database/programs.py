
class Programs:

    def __init__(self, programs):
        self.programs = programs


    def add_program(self, program):
        self.programs.append(program)

    def find_program(self, specification):
        # Finds a program with the following specification
        for a_program in self.programs:
            if specification(a_program):
                return a_program
        return None
