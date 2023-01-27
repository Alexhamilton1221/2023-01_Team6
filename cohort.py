
class Cohort:

    def __init__(self, name, program, term, number, count):
        # The name of the cohort
        self.name = name
        # The program of the cohort
        self.program = program
        # The Term of the cohort
        self.term = term
        # The number for the cohort (as in BCOM cohort 1 BCOM cohort 2
        self.number = number
        # The number of students in the cohort
        self.count = count

    def same_name(self, name):
        return self.name == name

    def same_program(self, program):
        return self.program == program

    def same_term(self, term):
        return self.term == term

    def same_number(self, number):
        return self.number == number

    def same_count(self, count):
        return self.count == count

