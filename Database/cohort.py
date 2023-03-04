
class Cohort:

    def __init__(self, program, term, number, count, courses, room = None, lab = None):
        # The program of the cohort (program class)
        self.program = program
        # The Term of the cohort (integer)
        self.term = term
        # The number for the cohort (as in BCOM cohort 1 BCOM cohort 2 (integer)
        self.number = number
        # The number of students in the cohort (integer)
        self.count = count
        # The Courses Taken By this cohort (array of course object)
        self.courses = courses
        # The room of the cohort (if applicable) (classroom object)
        self.room = room
        # The Lab of the cohort (if applicable) (classroom object)
        self.lab = lab

    def create_schedule(self):
        # This checks wether the course starts on the first day of the semester
        if self.program.is_core():
            starts_on = 1
        else:
            starts_on = 2

        if self.program.name == "FS":
            max_end_time = 20.50
        else:
            max_end_time = 16.50
        max_start_time = 8.50

        course_stack = []

        self.add_to_stack(course_stack, self.courses)
        self.stack_coreq_mover(course_stack)

        print(course_stack)

    def add_to_stack(self, queue, courses):
        # This adds a list of courses to a cohort queue
        for i in range(len(courses) - 1, -1, -1):
            not_in = True
            for q_course in queue:
                if q_course.is_equal(courses[i]):
                    not_in = False
                    break
            if not_in:
                queue.insert(0, courses[i])
                # adds the prerequisists
                self.add_to_stack(queue, courses[i].prerequisites)

    def stack_coreq_mover(self, stack):
        # This function moves the corequsits next to each other in the queue and after both of their respective
        for course in stack:
            extras = course.extra_req.split("|")
            coreq = ""
            for extra in extras:
                if extra.startswith("COREC"):
                    coreq = extra.split("=")[1]
            if not coreq == "":
                for c_course in stack:
                    if c_course.name == coreq:
                        stack.remove(c_course)
                        stack.insert(stack.index(course) - 1, c_course)
















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




