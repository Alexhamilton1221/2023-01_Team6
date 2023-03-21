from unittest import TestCase

from Database.cohorts import NearLimit
from Database.cohorts import OverLimit
from Database.programs import Programs
from hardCodedCourses import temp_create_courses
from Database.classrooms import Classrooms
from Database.classroom import Classroom
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

    def test_create_cohort_small_amount_type_assignReasableCohorts(self):
        programs = Programs(temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["PCOM 1", 67], ["BCOM 1", 20]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)
    def test_create_cohort__create_corhgorts_assignReasableCohorts(self):
        programs = Programs(temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["PCOM 1", 67], ["PCOM 2", 45],["PCOM 3", 28], ["BA 1", 46], ["BA 3", 30], ["DXD 2", 50], ["BK 1", 36]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)

        cohorts.show_cohorts()

    def test_near_limit_cohort_creation_assign_cohorts(self):
        programs = Programs(temp_create_courses())
        class1 = Classroom("1", 30)
        class2 = Classroom("2", 30)
        class3 = Classroom("1-lab", 30, True)
        classrooms = Classrooms([class1, class2, class3])
        cohorts = Cohorts()
        students = [["PCOM 1", 120]]
        cohorts.create_cohorts(classrooms, programs, students)

    def test_full_Stack_extra_assigne_cohorts(self):
        programs = Programs(temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["FS 1", 90]]
        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)

        cohorts.show_cohorts()

    def test_given_cohorts_make_schedules_for_all(self):
        programs = Programs(temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["PCOM 1", 67], ["PCOM 3", 45], ["BA 1", 46], ["BA 3", 30], ["DXD 2", 50],
                    ["BK 1", 36]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)

        cohorts.create_schedules(2)
        print(cohorts)

    def test_given_cohorts_make_schedules_for_all_large(self):
        programs = Programs(temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["PCOM 1", 67], ["PCOM 3", 63], ["BA 1", 46], ["BA 3", 30], ["DXD 2", 50],
                    ["BK 1", 36], ["FS 1", 90]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)

        cohorts.create_schedules(2)
        print(cohorts)


