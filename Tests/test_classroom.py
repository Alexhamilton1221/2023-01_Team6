from unittest import TestCase
import classroom as cl


class TestClassroom(TestCase):
    def test_is_equal(self):
        c1 = cl.Classroom("PC0102", 24)
        c2 = cl.Classroom("PC0102", 24)
        c3 = cl.Classroom("Td0203", 24, True)
        other = 5
        self.assertEqual(True, c1.is_equal(c2))
        self.assertEqual(False, c1.is_equal(c3))
        self.assertEqual(False, c1.is_equal(other))
