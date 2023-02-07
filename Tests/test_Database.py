
from unittest import TestCase
from Database.program import Program
from Database.cohort import Cohort
from Database.course import Course
from Database.lecture import Lecture
from Database.classroom import Classroom

class TestData(TestCase):

    def test_general(self):
        # This is more of a check for how the database is orgized than a real test
        PCOM = Program("PCOM")


        Cmpt101 = Course("Cmpt101", 8, [])
        Cmpt102 = Course("Cmpt102", 8, [Cmpt101])
        Cmpt130 = Course("Cmpt130", 3, [], "Online")


        cohort1 = Cohort(PCOM, 1, 1, 24, [Cmpt101, Cmpt102, Cmpt130])
        cohort1.generate_name()
        print(cohort1.name)

        room1 = Classroom("110-11", 24)
        room2 = Classroom("Online", 999)

        lecture1 = Lecture(room1, 8, 10)
        lecture2 = Lecture(room2, 10, 12)

        day1 = Day(False)

        cohort1.courses[0].add_lecture(lecture1)
        day1.add_lecture(lecture1)

        cohort1.courses[0].add_lecture(lecture2)
        day1.add_lecture(lecture2)