class Students:

    def __init__(self, students = []):
        # a list of all students
        self.students = students

    def get_students(self, specification):
        # Finds students with the following specification
        students = []
        for student in self.students:
            if specification(student):
                students.append(student)
        return students

    def get_counts(self, programs):
        # This gets the counts of the students in the [("PCOM 1", 54),("PCOM 2", 45), ("PCOM 3", 81), ("PC 2", 32)]
        # Note: This is an identical format to the students used by cohort creation
        students = []
        for program in programs.programs:
            # Creates a lambda for wether the program is core is not
            if program.is_core():
                comparator = lambda student: student.core == program
            else:
                comparator = lambda student: student.program == program


            for term in range(1, 4):
                students = self.get_students(lambda student: comparator(student) and student.term == term)
                count = len(students)
                if count > 0:
                    students.append((program.name + " " + str(term), count))

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







