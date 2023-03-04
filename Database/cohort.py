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

    def create_schedule(self):
        # COREQS
        # This checks wether the course starts on the first day of the semester
        if self.program.is_core():
            starts_on = 1
        else:
            starts_on = 2

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

        self.add_to_stack(course_stack, self.courses)
        self.stack_coreq_mover(course_stack)
        self.not_prereq_lower_priority(course_stack)

        i = 0
        while course_stack != []:
            course = course_stack[i]

            lecture_length = 1.5
            course_lecture_legnth = lecture_length
            day_min = 0
            class_count = len(course.lectures)

            if course.delivery == "Lab":
                occupied_room = self.lab
                unoccupied_room = self.room
            else:
                occupied_room = self.room
                unoccupied_room = self.lab

            unfinished_prereq = False
            corequsite = None

            extras = course.extra_req.split("|")
            for extra in extras:
                if extra.startswith("H"):
                    lecture_length = float(extra.split("=")[1])
                elif extra.startswith("T"):
                    day_min = 24
                elif extra.startswith("COREC"):
                    coreq = extra.split("=")[1]
                    for o_course in course_stack:
                        if o_course.name == coreq:
                            corequsite = o_course
                            for prec in o_course.prerequisites:
                                if prec in course_stack:
                                    i = self.course_stack_update_index(course_stack, prec, i)
                                    unfinished_prereq = True
            coreq_lecture_length = 0
            if unfinished_prereq:
                continue
            else:
                if corequsite is not None:
                    course_lecture_legnth = lecture_length
                    coreq_lecture_length = 1.5
                    extras = course.extra_req.split("|")
                    for extra in extras:
                        if extra.startswith("H"):
                            coreq_lecture_length = float(extra.split("=")[1])
                        elif extra.startswith("T"):
                            day_min = 24

                    lecture_length = course_lecture_legnth + coreq_lecture_length
                    if len(corequsite.lectures) > class_count:
                        class_count = len(corequsite.lectures)

                    latest_prereq = course.last_prereq_day()
                    if latest_prereq < corequsite.last_prereq_day():
                        latest_prereq = corequsite.last_prereq_day()
                    if day_min < latest_prereq:
                        day_min = latest_prereq




            cur_start_time = max_start_time + time_offset
            cur_end_time = lecture_length + max_start_time + time_offset

            start_day = starts_on + course.last_prereq_day()
            if start_day <= day_min:
                start_day = day_min + starts_on

            end_day = class_count * 2 + start_day
            start_lecture = Lecture(start_day, cur_start_time, cur_end_time)
            end_lecture = Lecture(end_day, cur_start_time, cur_end_time)

            # NOTE: THE online checks do not stop new lectures from being scheduled before or after
            while not occupied_room.check_if_lecture_fits(start_lecture) or not occupied_room.check_if_lecture_fits(
                    end_lecture) \
                    or self.has_time_conflict(start_day, end_day, cur_start_time, cur_end_time) \
                    or cur_end_time > max_end_time \
                    or (course.delivery == "Online"
                        and (self.has_time_conflict(start_day, end_day, max_start_time, cur_end_time) and self.has_time_conflict(start_day, end_day, cur_start_time, max_end_time))):


                # 48 is a temp value for the end of a term
                if end_day <= 48:
                    start_day += 2
                    end_day += 2
                else:

                    start_day = starts_on + course.last_prereq_day()
                    if start_day <= day_min:
                        start_day = day_min + starts_on
                    end_day = class_count * 2 + start_day
                    time_offset += time_change_mod
                    cur_start_time = max_start_time + time_offset
                    cur_end_time = lecture_length + cur_start_time

                start_lecture = Lecture(start_day, cur_start_time, cur_end_time)
                end_lecture = Lecture(end_day, cur_start_time, cur_end_time)

            if corequsite is None:
                course.set_lecture_time(cur_start_time, cur_end_time)
                j = 0
                for day in range(start_day, end_day, 2):
                    course.lectures[j].day = day
                    j += 1

                course_stack.remove(course)
            else:
                course.set_lecture_time(cur_start_time, cur_start_time + course_lecture_legnth)
                end_day = len(course.lectures) * 2 + start_day
                j = 0
                for day in range(start_day, end_day, 2):
                    course.lectures[j].day = day
                    j += 1

                course_stack.remove(course)

                corequsite.set_lecture_time(cur_start_time + course_lecture_legnth, cur_start_time + course_lecture_legnth + coreq_lecture_length)
                end_day = len(corequsite.lectures) * 2 + start_day
                j = 0
                for day in range(start_day, end_day, 2):
                    corequsite.lectures[j].day = day
                    j += 1

                course_stack.remove(corequsite)



            i = self.course_stack_update_index(course_stack, course, i)

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
            self.name = self.program.name + "0" + str(self.term) + "0" + str(self.number)
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
