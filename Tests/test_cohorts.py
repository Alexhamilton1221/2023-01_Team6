from unittest import TestCase
from Database.programs import Programs
from hardCodedCourses import temp_create_courses
from Database.classrooms import Classrooms
from hardCodedClassrooms import temp_Classroom_add
from Database.cohorts import Cohorts
from Database.cohort import Cohort

class TestCohorts(TestCase):
    def test_givenNewCohort_AddCohort_HaveChort(self):
        cohort = Cohort("1101", 1, 1, 24, [])
        cohorts = Cohorts()

        cohorts.add_cohort(cohort)
        gottenCohort = cohorts.cohorts[0]

        assert cohort == gottenCohort

    def test_create_cohort_Single_type_assignReasableCohorts(self):
        programs = Programs(temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["PCOM 1", 67]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)
    def test_create_cohort__create_corhgorts_assignReasableCohorts(self):
        programs = Programs(temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["PCOM 1", 67], ["PCOM 2", 56], ["PCOM 3", 28], ["BA 1", 25], ["BA 2", 43], ["BA 3", 30], ["FS 2", 17]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)

        cohorts.show_cohorts()

    



