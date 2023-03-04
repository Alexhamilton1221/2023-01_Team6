from unittest import TestCase
from Database import classroom as cl
from Database.cohort import Cohort
from Database.course import Course

from Database.lecture import Lecture
from Database.program import Program
from Database.programs import Programs
from hardCodedCourses import temp_create_courses


class TestClassroom(TestCase):
    def test_is_equal(self):
        c1 = cl.Classroom("PC0102", 24)
        c2 = cl.Classroom("PC0102", 24)
        c3 = cl.Classroom("Td0203", 24, True)
        other = 5
        self.assertEqual(True, c1.is_equal(c2))
        self.assertEqual(False, c1.is_equal(c3))
        self.assertEqual(False, c1.is_equal(other))

    def test_givenseperate_lecture_is_within_returnTrue(self):
        lecture1 = Lecture(0, 8.50, 10.50)
        lecture2 = Lecture(1, 8.50, 10.50)
        c1 = cl.Classroom("PC0102", 24)
        programs = Programs(temp_create_courses())
        course = [Course("pcl3", 24, [])]
        course[0].lectures = [lecture1]
        cohort1 = Cohort(programs.get_program(lambda x: x.name == "PCOM"), 1, 1, 20, course, c1)
        c1.add_cohort(cohort1)
        answer = c1.check_if_lecture_fits(lecture2)

        assert answer

    def test_givensame_lecture_is_within_returnTrue(self):
        lecture1 = Lecture(0, 8.50, 10.50)
        lecture2 = Lecture(1, 8.50, 10.50)
        c1 = cl.Classroom("PC0102", 24)
        programs = Programs(temp_create_courses())
        course = [Course("pcl3", 24, [])]
        course[0].lectures = [lecture1]
        cohort1 = Cohort(programs.get_program(lambda x: x.name == "PCOM"), 1, 1, 20, course, c1)
        c1.add_cohort(cohort1)
        answer = c1.check_if_lecture_fits(lecture1)

        assert answer == False
