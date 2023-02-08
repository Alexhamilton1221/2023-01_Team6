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

    def test_givenExtraSpaceReturnAmunts_Calc_cohort_capacity_returnNumber(self):
        room1 = Classroom("11032", 30)
        room2 = Classroom("11033 Lab", 29, True)
        rooms = Classrooms([room1, room2])

        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        cohort = Cohort(PCOM, 1, 1, 20, PCOM.get_instance_courses(lambda x: x.term == 1))
        cohorts = Cohorts([cohort])

        spare_space = calc_space.calc_cohort_capacity(rooms, cohorts)

        assert (cohort, 9) == spare_space[0]

    def test_majorTestofMultiple_Calc_cohort_capacity_returnNumber(self):
        # This creates the room for the test
        room1 = Classroom("11032", 30)
        room2 = Classroom("11033", 24)
        room3 = Classroom("11034", 30)
        room4 = Classroom("110", 30, True)
        rooms = Classrooms([room1, room2, room3, room4])

        # This creates the program for the tes
        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        BC = programs.get_program(lambda x: x.name == "BC")
        GLM = programs.get_program(lambda x: x.name == "GLM")

        # This creates the cohorts of the test
        # Core
        PCOMC1 = Cohort(PCOM, 1, 1, 28, PCOM.get_instance_courses(lambda x: x.term == 1))
        PCOMC2 = Cohort(PCOM, 1, 2, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        PCOMC3 = Cohort(PCOM, 2, 1, 25, PCOM.get_instance_courses(lambda x: x.term == 2))
        PCOMC4 = Cohort(PCOM, 3, 1, 30, PCOM.get_instance_courses(lambda x: x.term == 3))

        # Program
        BC1 = Cohort(BC, 1, 1, 28, BC.get_instance_courses(lambda x: x.term == 1))
        BC2 = Cohort(BC, 2, 1, 20, BC.get_instance_courses(lambda x: x.term == 2))
        GLM1 = Cohort(GLM, 1, 1, 22, BC.get_instance_courses(lambda x: x.term == 1))

        cohorts = Cohorts([PCOMC1, PCOMC2, PCOMC3, PCOMC4, BC1, BC2, GLM1])
        for cohort in cohorts.cohorts:
            cohort.generate_name()

        space_core_class_space = calc_space.calc_cohort_hours(rooms, cohorts, core=True, lab=False)
        space_core_lab_space = calc_space.calc_cohort_hours(rooms, cohorts, core=True, lab=True)

        space_program_class_space = calc_space.calc_cohort_hours(rooms, cohorts, core=False, lab=False)
        space_program_lab_space = calc_space.calc_cohort_hours(rooms, cohorts, core=False, lab=True)

        extra_cohort_room = calc_space.calc_cohort_capacity(rooms, cohorts)
        assert [(PCOMC1, 2), (BC1, 2), (GLM1, 8)] == extra_cohort_room

    def test_givenClassroomsandCohorts_CalcprogramRoom_ShowCapacity(self):
        # This creates the room for the test
        room1 = Classroom("11032", 30)
        room2 = Classroom("11033", 24)
        room3 = Classroom("11034", 30)
        room4 = Classroom("11032 Computer Lab", 30, True)
        rooms = Classrooms([room1, room2, room3, room4])

        # This creates the program for the tes
        programs = Programs(hardCodedCourses.temp_create_courses())
        PCOM = programs.get_program(lambda x: x.name == "PCOM")
        BC = programs.get_program(lambda x: x.name == "BC")
        GLM = programs.get_program(lambda x: x.name == "GLM")

        # This creates the cohorts of the test
        # Core
        PCOMC1 = Cohort(PCOM, 1, 1, 28, PCOM.get_instance_courses(lambda x: x.term == 1))
        PCOMC2 = Cohort(PCOM, 1, 2, 30, PCOM.get_instance_courses(lambda x: x.term == 1))
        PCOMC3 = Cohort(PCOM, 2, 1, 25, PCOM.get_instance_courses(lambda x: x.term == 2))
        PCOMC4 = Cohort(PCOM, 3, 1, 30, PCOM.get_instance_courses(lambda x: x.term == 3))
        PCOMC5 = Cohort(PCOM, 3, 2, 24, PCOM.get_instance_courses(lambda x: x.term == 3))

        # Program
        BC1 = Cohort(BC, 1, 1, 28, BC.get_instance_courses(lambda x: x.term == 1))
        BC2 = Cohort(BC, 2, 1, 20, BC.get_instance_courses(lambda x: x.term == 2))
        GLM1 = Cohort(GLM, 1, 1, 22, BC.get_instance_courses(lambda x: x.term == 1))

        cohorts = Cohorts([PCOMC1, PCOMC2, PCOMC3, PCOMC4, PCOMC5, BC1, BC2, GLM1])
        for cohort in cohorts.cohorts:
            cohort.generate_name()

        calc_space.calc_program_room(programs, rooms, cohorts)

