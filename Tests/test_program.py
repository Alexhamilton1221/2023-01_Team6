from unittest import TestCase
from Database.program import Program
from Database.storedcourse import StoredCourse
from Database.course import Course


class TestProgram(TestCase):


    def test_whereNoSecifcationGiven_gethours_getallhoursofYear(self):
        # Bookkeeping Certificate
        BC = Program("BC")
        # Term 1
        BC.add_course(StoredCourse("ACCT 0201", 18, 1, []))
        BC.add_course(StoredCourse("ACCT 0202", 12, 1, []))
        BC.add_course(StoredCourse("ACCT 0203", 12, 1, []))
        # Term 2
        BC.add_course(StoredCourse("ACCT 0206", 12, 2, []))
        BC.add_course(StoredCourse("ACCT 0210", 28, 2, [], "Lab"))
        BC.add_course(StoredCourse("ACCT 0211", 28, 12, [], "Lab"))
        # Term 3
        BC.add_course(StoredCourse("SCMT 0505", 21, 3, []))
        BC.add_course(StoredCourse("PCOM 0151", 33, 3, [], "Class", "H=3h"))

        hours = BC.get_hours()

    def test_whereOneTermSecifcationGiven_gethours_getTerm1hourse(self):
        # Bookkeeping Certificate
        BC = Program("BC")
        # Term 1
        BC.add_course(StoredCourse("ACCT 0201", 18, 1, []))
        BC.add_course(StoredCourse("ACCT 0202", 12, 1, []))
        BC.add_course(StoredCourse("ACCT 0203", 12, 1, []))
        # Term 2
        BC.add_course(StoredCourse("ACCT 0206", 12, 2, []))
        BC.add_course(StoredCourse("ACCT 0210", 28, 2, [], "Lab"))
        BC.add_course(StoredCourse("ACCT 0211", 28, 12, [], "Lab"))
        # Term 3
        BC.add_course(StoredCourse("SCMT 0505", 21, 3, []))
        BC.add_course(StoredCourse("PCOM 0151", 33, 3, [], "Class", "H=3h"))

        hours = BC.get_hours(lambda x: x.term == 1)

        assert 42 == hours

    def test_whereLabhours_gethours_getLabhourse(self):
        # Bookkeeping Certificate
        BC = Program("BC")
        # Term 1
        BC.add_course(StoredCourse("ACCT 0201", 18, 1, []))
        BC.add_course(StoredCourse("ACCT 0202", 12, 1, []))
        BC.add_course(StoredCourse("ACCT 0203", 12, 1, []))
        # Term 2
        BC.add_course(StoredCourse("ACCT 0206", 12, 2, []))
        BC.add_course(StoredCourse("ACCT 0210", 28, 2, [], "Lab"))
        BC.add_course(StoredCourse("ACCT 0211", 28, 12, [], "Lab"))
        # Term 3
        BC.add_course(StoredCourse("SCMT 0505", 21, 3, []))
        BC.add_course(StoredCourse("PCOM 0151", 33, 3, [], "Class", "H=3h"))

        hours = BC.get_hours(lambda x: x.delivery == "Lab")

        assert 56 == hours

    def test_whereLabandTerm_gethours_getLabandTermhourse(self):
        # Bookkeeping Certificate
        BC = Program("BC")
        # Term 1
        BC.add_course(StoredCourse("ACCT 0201", 18, 1, []))
        BC.add_course(StoredCourse("ACCT 0202", 12, 1, []))
        BC.add_course(StoredCourse("ACCT 0203", 12, 1, [], "Lab"))
        # Term 2
        BC.add_course(StoredCourse("ACCT 0206", 12, 2, []))
        BC.add_course(StoredCourse("ACCT 0210", 28, 2, [], "Lab"))
        BC.add_course(StoredCourse("ACCT 0211", 28, 12, [], "Lab"))
        # Term 3
        BC.add_course(StoredCourse("SCMT 0505", 21, 3, []))
        BC.add_course(StoredCourse("PCOM 0151", 33, 3, [], "Class", "H=3h"))

        hours = BC.get_hours(lambda x: x.delivery == "Lab" and x.term == 1)

        assert 12 == hours

    def test_getInstanceCourses_showallCourses(self):
        # Bookkeeping Certificate
        BC = Program("BC")
        # Term 1
        BC.add_course(StoredCourse("ACCT 0201", 18, 1, []))
        BC.add_course(StoredCourse("ACCT 0202", 12, 1, []))
        BC.add_course(StoredCourse("ACCT 0203", 12, 1, [], "Lab"))
        # Term 2
        BC.add_course(StoredCourse("ACCT 0206", 12, 2, []))
        BC.add_course(StoredCourse("ACCT 0210", 28, 2, [], "Lab"))
        BC.add_course(StoredCourse("ACCT 0211", 28, 12, [], "Lab"))
        # Term 3
        BC.add_course(StoredCourse("SCMT 0505", 21, 3, []))
        BC.add_course(StoredCourse("PCOM 0151", 33, 3, [], "Class", "H=3h"))

        courses = BC.get_instance_courses()

        for course in courses:
            assert type(course) == Course

    def test_givenCore_is_core_showTrue(self):
        # Bookkeeping Certificate
        BCOM = Program("BCOM")

        output = BCOM.is_core()

        assert output
