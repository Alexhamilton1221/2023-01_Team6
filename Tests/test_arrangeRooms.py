from unittest import TestCase

import calc_space
import hardCodedCourses
from Database.programs import Programs
from Database.program import Program
from Database.classroom import Classroom
from Database.classrooms import Classrooms
from Database.cohort import Cohort
from Database.cohorts import Cohorts

class Test(TestCase):
    def test_givenASingleRoom_CalcHours_showremainghours(self):
        room1 = Classroom("11032", 30)
        rooms = Classrooms([room1])

        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        cohort = Cohort(PCOM, 1, 1, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        cohorts = Cohorts([cohort])

        spare_rooms = calc_space.calc_cohort_hours(rooms, cohorts, True, False)

        assert (room1, 122) == spare_rooms[0]

    def test_givenMultipleRooms_CalcHours_showremainghours(self):
        room1 = Classroom("11032", 30)
        room2 = Classroom("11033", 30)
        rooms = Classrooms([room1, room2])

        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        cohort = Cohort(PCOM, 1, 1, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        cohorts = Cohorts([cohort])

        spare_rooms = calc_space.calc_cohort_hours(rooms, cohorts, True, False)

        assert (room1, 122) == spare_rooms[0]
        assert (room2, 192) == spare_rooms[1]

    def test_givenMultipleCohorts_CalcHours_shownohours(self):
        room1 = Classroom("11032", 30)
        rooms = Classrooms([room1])

        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        cohort1 = Cohort(PCOM, 1, 1, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        cohort2 = Cohort(PCOM, 1, 2, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        cohorts = Cohorts([cohort1, cohort2])

        spare_rooms = calc_space.calc_cohort_hours(rooms, cohorts, True, False)

        assert [] == spare_rooms

    def test_givenroomamount_Calc_students_showamounts(self):
        room1 = Classroom("11032", 30)
        rooms = Classrooms([room1])

        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        cohort = Cohort(PCOM, 1, 1, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        cohorts = Cohorts([cohort])

        spare_rooms = calc_space.calc_cohort_hours(rooms, cohorts, True, False)
        students = calc_space.calc_extra_students(spare_rooms[0][1], 70, spare_rooms[0][0].size)

        # There is room for 30 more students
        assert 30 == students

    def test_givenRoomsWithClassAndLabs_Calc_students_Classes_ShowAmounts(self):
        room1 = Classroom("11032", 30)
        room2 = Classroom("11032", 30, True)
        rooms = Classrooms([room1, room2])

        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        cohort = Cohort(PCOM, 1, 1, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        cohorts = Cohorts([cohort])

        spare_rooms = calc_space.calc_cohort_hours(rooms, cohorts, True, False)
        students = calc_space.calc_extra_students(spare_rooms[0][1], 70, spare_rooms[0][0].size)

        # There is room for 30 more students
        assert 30 == students

    def test_givenRoomsWithClassAndLabs_Calc_students_labs_ShowAmounts(self):
        room1 = Classroom("11032", 30)
        room2 = Classroom("11032", 30, True)
        rooms = Classrooms([room1, room2])

        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        cohort = Cohort(PCOM, 1, 1, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        cohorts = Cohorts([cohort])

        spare_rooms = calc_space.calc_cohort_hours(rooms, cohorts, True, True)
        students = calc_space.calc_extra_students(spare_rooms[0][1], 70, spare_rooms[0][0].size)

        # There is room for 60 more students
        assert 60 == students

