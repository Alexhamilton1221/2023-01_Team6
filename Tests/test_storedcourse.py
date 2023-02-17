from unittest import TestCase

from Database.storedcourse import StoredCourse
from Database.course import Course
class TestStoredCourse(TestCase):
    def test_givenNoPrerequsits_generateCourse_createCorrectCourse(self):
        StoredCourse1 = StoredCourse("C1", 10, 1, [])
        Course1 = Course("C1", 10, [])
        genCourse = StoredCourse1.generate_course()

        answer = Course1.is_equal(genCourse)

        assert answer == True
