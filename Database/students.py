class Students:

    def __init__(self, students):
        # a list of all students
        self.students = students

    def get_students(self, specification):
        # Finds students with the following specification
        students = []
        for student in self.students:
            if specification(student):
                students.append(student)
        return students
    def add_to_cohorts(self, programs, cohorts):
        # Adds the students to each cohort
        for program in programs.programs:
            # Creates a lambda for wether the program is core is not
            if program.is_core():
                comparator = lambda student: student.core == program
            else:
                comparator = lambda student: student.program == program

            for term in range(1, 4):
                students = self.get_students(lambda student: comparator(student) and student.term == term)
                for cohort in cohorts.get_cohorts(lambda cohort: cohort.program == program and cohort.term == term):
                    cohort.add_students(students)







