import math

import hardcodedother
from Database.lecture import Lecture


class Cohort:

    def __init__(self, program, term, number, count, courses, room=None, lab=None):
        # The program of the cohort (program class)
        self.program = program
        # The Term of the cohort (integer)
        self.term = term
        # The number for the cohort (as in BCOM cohort 1 BCOM cohort 2 (integer)
        self.number = number
        # The number of students in the cohort (integer)
        self.count = count
        # The Courses Taken By this cohort (array of course object)
        self.courses = courses
        # The room of the cohort (if applicable) (classroom object)
        self.room = room
        # The Lab of the cohort (if applicable) (classroom object)
        self.lab = lab
        # The students in the cohort
        self.students = []


    def create_schedule(self, cur_semester):
        # This creates the schedules for the cohorts of the term
        # var term is the term of this semester fall, winter, or sprint

        holidays = hardcodedother.get_holidays(cur_semester)
        term_length = hardcodedother.get_term_length(cur_semester)
        # This checks whether the course starts on the first day of the semester or the second
        if self.program.is_core():
            starts_on = 3
        else:
            starts_on = 4

        # Sets the fullstack courses to start in the evening and move towards the morning, while all others
        # Start in the morning and move towards the evening
        if self.program.name == "FS":
            max_end_time = 20.50
            time_change_mod = -0.5
            time_offset = 10.5
        else:
            max_end_time = 16.50
            time_change_mod = 0.5
            time_offset = 0
        max_start_time = 8.50


        course_stack = []
        # This arranges the courses to make the scheduling make more sense, corequisites are moved next to each other,
        # and courses that are not prerequisites to any course are assigned last
        self.add_to_stack(course_stack, self.courses)
        self.stack_coreq_mover(course_stack)
        self.not_prereq_lower_priority(course_stack)

        i = 0
        # Keeps looping until all courses in the stack are gone
        while course_stack != []:
            course = course_stack[i]

            lecture_length = 1.5
            course_lecture_length = lecture_length
            day_min = 0
            class_count = len(course.lectures)

            # Chooses the room that the course is in
            if course.delivery == "Lab":
                occupied_room = self.lab
            else:
                occupied_room = self.room

            unfinished_prereq = False
            corequsite = None

            # This code checks for any additional specification that the course may have, such as course length
            # that it has to start halfway through the term, or that it has a corequisite
            extras = course.extra_req.split("|")
            for extra in extras:
                if extra.startswith("H"):
                    lecture_length = float(extra.split("=")[1])
                elif extra.startswith("T"):
                    day_min = math.ceil(term_length/2)
                elif extra.startswith("COREC"):
                    coreq = extra.split("=")[1]
                    # This go through all the courses in the stack to find the corequisite, and if it find the
                    # corequisite checks if any of the prerequisite of the corequisite have not been finished yet,
                    # if so, does them first, else continuous with the corequisite
                    for o_course in course_stack:
                        if o_course.name == coreq:
                            corequsite = o_course
                            for prec in o_course.prerequisites:
                                if prec in course_stack:
                                    i = self.course_stack_update_index(course_stack, prec, i)
                                    unfinished_prereq = True
            coreq_lecture_length = 0
            # loops again if the corequisite had an unfinished prerequisite
            if unfinished_prereq:
                continue
            else:
                # When a course has a corequsite, it effectivly treats both courses as one giant couse that takes the
                # time for both courses, and it will pretend like it lasts for the longer of the two
                if corequsite is not None:
                    course_lecture_length = lecture_length
                    coreq_lecture_length = 1.5
                    extras = course.extra_req.split("|")
                    for extra in extras:
                        if extra.startswith("H"):
                            coreq_lecture_length = float(extra.split("=")[1])
                        elif extra.startswith("T"):
                            day_min = math.ceil(term_length/2)

                    lecture_length = course_lecture_length + coreq_lecture_length
                    if len(corequsite.lectures) > class_count:
                        class_count = len(corequsite.lectures)

                    latest_prereq = course.last_prereq_day()
                    if latest_prereq < corequsite.last_prereq_day():
                        latest_prereq = corequsite.last_prereq_day()
                    if day_min < latest_prereq:
                        day_min = latest_prereq

            # The start time of the lecture is the start time + the amount of time the lectures are shifted by
            # The end is the same + the length of the lecture
            cur_start_time = max_start_time + time_offset
            cur_end_time = lecture_length + max_start_time + time_offset

            # The start day is either the first or second day, + what ever courses prerequssits, so it never starts
            # Too early
            start_day = starts_on + course.last_prereq_day()
            if start_day <= day_min:
                start_day = day_min + starts_on
            # courses go every other day
            end_day = class_count * 2 + start_day
            for i in range(0, len(holidays)):
                if start_day <= holidays[i] <= end_day and end_day % 2 == holidays[i] % 2:
                    end_day += 2


            time_resets = 0
            # NOTE: THE online checks do not stop new lectures from being scheduled before or after
            # might cause issues later
            while not occupied_room.check_if_lecture_fits(start_day, end_day, cur_start_time, cur_end_time) \
                    or self.has_time_conflict(start_day, end_day, cur_start_time, cur_end_time) \
                    or cur_end_time > max_end_time \
                    or (course.delivery == "Online"
                        and (self.has_time_conflict(start_day, end_day, max_start_time, cur_end_time) and self.has_time_conflict(start_day, end_day, cur_start_time, max_end_time))):


                # 48 is a temp value for the end of a term, to be replaced once more concise data, also needs to check
                # for holidays
                if end_day <= term_length:
                    if start_day in holidays:
                        end_day -= 2
                    start_day += 2

                    end_day += 2
                    old_end = end_day
                    for i in range(0, len(holidays)):
                        if old_end <= holidays[i] <= end_day and end_day % 2 == holidays[i] % 2:
                            end_day += 2
                    if end_day > term_length:
                        continue

                        # DEBUG
                    if course.name == "CMSK 0233" and start_day == 15 and cur_start_time == 12.5:
                        print("ON")
                else:
                    # If it can't fit a lecture by a time no where in the semester, will go to the next time slot 30 later (or before for full stack)
                    start_day = starts_on + course.last_prereq_day()
                    if start_day <= day_min:
                        start_day = day_min + starts_on
                    end_day = class_count * 2 + start_day
                    for i in range(0, len(holidays)):
                        if start_day <= holidays[i] <= end_day and end_day % 2 == holidays[i] % 2:
                            end_day += 2
                    time_offset += time_change_mod
                    cur_start_time = max_start_time + time_offset
                    cur_end_time = lecture_length + cur_start_time
                    if (self.program.name != "FS" and cur_end_time > max_end_time) or (self.program.name == "FS" and cur_start_time < max_start_time):
                        time_resets += 1
                        if time_resets == 3:
                            raise ValueError
                        if self.program.name == "FS":
                            time_offset = 10.5
                        else:
                            time_offset = 0

                        cur_start_time = max_start_time + time_offset
                        cur_end_time = lecture_length + max_start_time + time_offset

            # Removes the one course from the stack and sets the time,
            if corequsite is None:
                course.set_lecture_time(cur_start_time, cur_end_time)
                j = 0
                for day in range(start_day, end_day, 2):
                    if day not in holidays:
                        course.lectures[j].day = day
                        j += 1

                course_stack.remove(course)
            else:
                # Sets time for both courses if it has a corequsite
                course.set_lecture_time(cur_start_time, cur_start_time + course_lecture_length)
                end_day = len(course.lectures) * 2 + start_day
                j = 0
                for day in range(start_day, end_day, 2):
                    if day not in holidays:
                        course.lectures[j].day = day
                        j += 1
                course.remove_day_zero_lectures()
                course_stack.remove(course)

                corequsite.set_lecture_time(cur_start_time + course_lecture_length, cur_start_time + course_lecture_length + coreq_lecture_length)
                end_day = len(corequsite.lectures) * 2 + start_day
                j = 0
                for day in range(start_day, end_day, 2):
                    if day not in holidays:
                        corequsite.lectures[j].day = day
                        j += 1

                corequsite.remove_day_zero_lectures()
                course_stack.remove(corequsite)
            # This sets the next index of the loop.
            i = self.course_stack_update_index(course_stack, course, i)

    def add_students(self, students):
        # Adds a list of students to the cohort if they fit
        while len(students) != 0 and len(self.students) < self.count:
            student = students.pop(0)
            self.students.append(student)
            if self.program.is_core():
                student.core_cohort = self
            else:
                student.program_cohort = self


    def create_empty_lectures(self):
        # creates the empty lectures in the cohort
        for course in self.courses:
            course.create_empty_lectures()

    def course_stack_update_index(self, course_stack, course, i):
        # This is for setting the index in every loop of the course stack
        # IT moves the index to the after pre
        set_index = False
        for o_course in course_stack:
            is_prerequisite = False
            for preq in o_course.prerequisites:
                if preq.is_equal(course):
                    is_prerequisite = True
            if is_prerequisite:
                set_index = True
                found_new_prerequisite = False
                for preq in o_course.prerequisites:
                    for checked in course_stack:
                        if preq.is_equal(checked):
                            i = course_stack.index(preq)
                            found_new_prerequisite = True
                if not found_new_prerequisite:
                    i = course_stack.index(o_course)

        if not set_index:
            i = 0

        return i


    def add_to_stack(self, queue, courses):
        # This adds a list of courses to a cohort queue
        for i in range(len(courses) - 1, -1, -1):
            not_in = True
            for q_course in queue:
                if q_course.is_equal(courses[i]):
                    not_in = False
                    break
            if not_in:
                queue.insert(0, courses[i])
                # adds the prerequisists
                self.add_to_stack(queue, courses[i].prerequisites)

    def stack_coreq_mover(self, stack):
        # This function moves the corequsits next to each other in the queue and after both of their respective

        # Noted issues, core rqusitques effectivly "cycle" until they reach the back of stack
        for course in stack:
            extras = course.extra_req.split("|")
            coreq = ""
            for extra in extras:
                if extra.startswith("COREC"):
                    coreq = extra.split("=")[1]
            if not coreq == "":
                for c_course in stack:
                    if c_course.name == coreq:
                        stack.remove(course)
                        stack.insert(stack.index(c_course), course)

    def not_prereq_lower_priority(self, course_stack):
        # This function moves courses that are not prequsits to any course to be assigned last since they are the least
        # Important
        for course in course_stack:
            not_prereq = True
            for o_course in course_stack:
                if course in o_course.prerequisites:
                    not_prereq = False
                    break
            if not_prereq:
                course_stack.remove(course)
                course_stack.append(course)


    def has_time_conflict(self, start_day, end_day, start_time, end_time):
        # This checks if the course has a time conflict with itself
        start_lecture = Lecture(start_day, start_time, end_time)
        end_lecture = Lecture(end_day, start_time, end_time)

        for course in self.courses:
            for lecture in course.lectures:
                if lecture.is_within(start_lecture) or lecture.is_within(end_lecture):
                    return True
        return False

    def set_room(self, room):
        # Sets the room of the cohort
        self.room = room

    def set_lab(self, lab):
        # Sets the lab of the cohort
        self.lab = lab

    def generate_name(self):
        # Checks if there are over 10 cohorts in one program (extremely unlikely) to make the name correct
        if self.number < 10:
            self.name = self.program.name + str(self.term) + str(self.number)
        else:
            self.name = self.program.name + "0" + str(self.term) + str(self.number)

    def get_hours(self, specification=lambda x: True):
        # Gets the total number of courses in hours
        hours = 0
        for course in self.courses:
            if specification(course):
                hours += course.total_hours

        return hours

    def get_hours_remaining(self):
        # Gets the remaining number of courses in hours
        hours = 0
        for course in self.courses:
            hours += course.hours_remaining

    def same_name(self, name):
        return self.name == name

    def same_program(self, program):
        return self.program == program

    def same_term(self, term):
        return self.term == term

    def same_number(self, number):
        return self.number == number

    def same_count(self, count):
        return self.count == count

    def __str__(self):
        return self.name
