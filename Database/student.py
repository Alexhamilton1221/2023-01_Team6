
class Student:

    def __init__(self, id, name, term, core, core_cohort, program, program_cohort):
        # The student id of the student
        self.id = id
        # The name of the student
        self.name = name
        # The term of the student
        self.term = term
        # The core program of the student
        self.core = core
        # The core cohort of the student
        self.core_cohort = core_cohort
        # The program of the student
        self.program = program
        # The program cohort of the student
        self.program_cohort = program_cohort

    def __repr__(self) -> str:
        return "Id: " + str(self.id) + "\nName: " + self.name  + "\nCore: "\
            + str(self.core) + "\n\tCohort: " + str(self.core_cohort)+ "\nProgram: "\
            + str(self.program) + "\n\tCohort: " + str(self.program_cohort)



