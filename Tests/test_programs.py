from unittest import TestCase

import hardCodedCourses
from Database.program import Program
from Database.programs import Programs

class TestPrograms(TestCase):
    def test_givenAName_findProgram_returnthefoundProgram(self):
        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.programs[0]

        foundProgram = programs.get_program(lambda x: x.name == "PCOM")

        assert PCOM == foundProgram

    def test_givennotExist_findProgram_returnNone(self):
        programs = Programs(hardCodedCourses.temp_create_courses())

        foundProgram = programs.get_program(lambda x: x.name == "PCssOM")

        assert None == foundProgram

    def test_givehourse_findProgram_returnNone(self):
        programs = Programs(hardCodedCourses.temp_create_courses())

        programs.show_hours()

        # This test is for displaying the printing
        assert True