
class Cohort:

    def __init__(self, program, term, number, count, courses, room = None, lab = None):
        # The program of the cohort
        self.program = program
        # The Term of the cohort
        self.term = term
        # The number for the cohort (as in BCOM cohort 1 BCOM cohort 2
        self.number = number
        # The number of students in the cohort
        self.count = count
        # The Courses Taken By this cohort
        self.courses = courses
        # The room of the cohort (if applicable)
        self.room = room
        # The Lab of the cohort (if applicable)
        self.lab = lab

    def set_room(self, room):
        # Sets the room of the cohort
        self.room = room

    def set_lab(self, lab):
        # Sets the lab of the cohort
        self.lab = lab
    def generate_name(self):
        # Checks if there are over 10 cohorts in one program (extremely unlikely) to make the name correct
        if self.number < 10:
            self.name = self.program.name + "0" + str(self.term) + "0" + str(self.number)
        else:
            self.name = self.program.name + "0" + str(self.term) + str(self.number)

    def get_hours(self, specification=lambda x: True):
        # Gets the total number of courses in hours
        hours = 0
        for course in self.courses:
            if specification(course):
                hours += course.total_hours

        return hours

    def get_hours_remaining(self):
        # Gets the remaining number of courses in hours
        hours = 0
        for course in self.courses:
            hours += course.hours_remaining

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



