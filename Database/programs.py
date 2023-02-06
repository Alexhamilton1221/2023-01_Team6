
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

    def show_hours(self):
        # Shows hours separated by information
        for a_program in self.programs:
            print(a_program.name + ":")
            for term in range(1, 4):
                print("  Term " + str(term) + ":")
                print("     Class Hours: " + str(a_program.get_hours(lambda x: x.term == term and x.delivery == "Class")))
                print("     Lab Hours: " + str(a_program.get_hours(lambda x: x.term == term and x.delivery == "Lab")))
