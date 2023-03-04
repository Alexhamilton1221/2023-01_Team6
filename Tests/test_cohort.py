from unittest import TestCase

import hardCodedCourses
from Database.classrooms import Classrooms
from Database.cohort import Cohort
from Database.cohorts import Cohorts
from Database.lecture import Lecture
from Database.program import Program
from Database.classroom import Classroom
from Database.programs import Programs
from hardCodedClassrooms import temp_Classroom_add


class TestCohort(TestCase):
    def test_givenPCOMTerm1CLass_GenerateName_MakePCOM0101(self):
        PCOM = Program("PCOM")
        classroom = Classroom("DNE", 24)
        c1 = Cohort(PCOM, 1, 1, 24, "DNM")

        c1.generate_name()

        assert c1.name == "PCOM0101"

    def test_givenBCOM_GenerateName_MakeBCOM0101(self):
        BCOM = Program("BCOM")
        classroom = Classroom("DNE", 24)
        c1 = Cohort(BCOM, 1, 1, 24, "DNM")

        c1.generate_name()

        assert c1.name == "BCOM0101"

    def test_givenOver10Cohorts_GenerateName_MakeBCOM0110(self):
        BCOM = Program("BCOM")
        classroom = Classroom("DNE", 24)
        c1 = Cohort(BCOM, 1, 10, 24, "DNM")

        c1.generate_name()

        assert c1.name == "BCOM0110"

    def test_givencohortwithcoureses_gethours_showhours(self):
        PCOM = hardCodedCourses.temp_create_courses()[0]

        c1 = Cohort(PCOM, 1, 1, 24, PCOM.get_instance_courses(lambda x: x.term == 1))

        output = c1.get_hours(lambda x: x.is_lab() == False)

        assert 70 == output

    def test_create_squdule_with_prequisits_correct_show_squdule(self):

        programs = Programs(hardCodedCourses.temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["PCOM 1", 67]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)
        fakeLectures = [[], [], [], [], []]
        for i in range(0, 10):
            fakeLectures[0].append(Lecture(0, 0, 0))
        for i in range(0, 10):
            fakeLectures[1].append(Lecture(0, 0, 0))
        for i in range(0, 5):
            fakeLectures[2].append(Lecture(0, 0, 0))
        for i in range(0, 3):
            fakeLectures[3].append(Lecture(0, 0, 0))
        for i in range(0, 2):
            fakeLectures[4].append(Lecture(0, 0, 0))
        c1 = cohorts.cohorts[0]
        for i in range(0, 5):
            c1.courses[i].lectures = fakeLectures[i]
        c1.create_schedule()
        c1.generate_name()

    def test_create_squdule_with_fullstack_correct_show_squdule(self):

        programs = Programs(hardCodedCourses.temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["FS 2", 20]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)
        fakeLectures = [[], [], [], [], []]
        for i in range(0, 10):
            fakeLectures[0].append(Lecture(0, 0, 0))
        for i in range(0, 10):
            fakeLectures[1].append(Lecture(0, 0, 0))
        for i in range(0, 5):
            fakeLectures[2].append(Lecture(0, 0, 0))
        for i in range(0, 3):
            fakeLectures[3].append(Lecture(0, 0, 0))
        for i in range(0, 2):
            fakeLectures[4].append(Lecture(0, 0, 0))

        c1 = cohorts.cohorts[0]
        for i in range(0, 5):
            c1.courses[i].lectures = fakeLectures[i]
        c1.create_schedule()
        c1.generate_name()

    def test_create_squdule_with_online_correct_show_squdule(self):

        programs = Programs(hardCodedCourses.temp_create_courses())
        classrooms = Classrooms(temp_Classroom_add())
        students = [["BCOM 3", 20]]

        cohorts = Cohorts()
        cohorts.create_cohorts(classrooms, programs, students)
        fakeLectures = [[], [], [], [], [], []]
        for i in range(0, 10):
            fakeLectures[0].append(Lecture(0, 0, 0))
        for i in range(0, 10):
            fakeLectures[1].append(Lecture(0, 0, 0))
        for i in range(0, 5):
            fakeLectures[2].append(Lecture(0, 0, 0))
        for i in range(0, 3):
            fakeLectures[3].append(Lecture(0, 0, 0))
        for i in range(0, 2):
            fakeLectures[4].append(Lecture(0, 0, 0))
        for i in range(0, 7):
            fakeLectures[5].append(Lecture(0, 0, 0))
        c1 = cohorts.cohorts[0]
        for i in range(0, 6):
            c1.courses[i].lectures = fakeLectures[i]
        c1.create_schedule()
        c1.generate_name()
