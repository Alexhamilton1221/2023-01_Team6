from unittest import TestCase

import hardCodedCourses
from Database.cohort import Cohort
from Database.program import Program
from Database.classroom import Classroom
from Database.programs import Programs


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

    def test_create_squdule_correct_show_squdule(self):
        PCOM = hardCodedCourses.temp_create_courses()[0]

        c1 = Cohort(PCOM, 1, 1, 24, PCOM.get_instance_courses(lambda x: x.term == 1))
        c1.create_schedule()

    def test_create_squdule_with_prequisits_correct_show_squdule(self):
        programs = Programs(hardCodedCourses.temp_create_courses())
        FS = programs.get_program(lambda p: p.name == "FS")
        c1 = Cohort(FS, 1, 1, 24, FS.get_instance_courses(lambda x: x.term == 2))
        c1.create_schedule()


