from unittest import TestCase

from Database.cohort import Cohort
from Database.programs import Programs
from Database.student import Student
from hardCodedCourses import temp_create_courses
from hardCodedClassrooms import temp_Classroom_add


class TestStudent(TestCase):
    def test_reprenstion_Of_student(self):
        programs = Programs(temp_create_courses())
        PCOM = programs.get_program(lambda program: program.name == "PCOM")
        FS = programs.get_program(lambda program: program.name == "FS")
        cohort1 = Cohort(PCOM, 1, 1, 12, [])
        cohort1.generate_name()
        cohort2 = Cohort(FS, 1, 1, 30, [])
        cohort2.generate_name()
        student1 = Student(1111032, "Jeffy lindshaw", 1, PCOM, cohort1, FS, cohort2)  # add assertion here
        print(student1)



