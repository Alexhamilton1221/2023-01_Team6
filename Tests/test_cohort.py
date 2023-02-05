from unittest import TestCase
from Database.cohort import Cohort
from Database.program import Program
from Database.classroom import Classroom

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
