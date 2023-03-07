import math
import re

from Database.lecture import Lecture


class Course:
    # This is the single instance of a course
    def __init__(self, name, total_hours, prerequisites, delivery = "Class", extra_req = ""):
        # The name of the course (String)
        self.name = name
        # The total number of hours for this course (double)
        self.total_hours = total_hours
        # how many hours are left in the course (double)
        self.hours_remaining = total_hours
        # The prequisites of this course (array of courses)
        self.prerequisites = prerequisites
        # How the course is delivered (Class, Lab, Online, Virtual) (online is synchronous, Virtual is async) (String)
        self.delivery = delivery
        # Lectures the course has taken (array of lecture object)
        self.lectures = []
        # extra requirements for this course
        self.extra_req = extra_req
        # Whether the course has finished all lectures (boolean)
        self.finished = False

    def add_lecture(self, lecture):
        # Adds a new lecture to lectures
        self.hours_remaining -= lecture.length()
        self.lectures.append(lecture)
        if self.hours_remaining <= 0:
            self.finished = True

    def set_lecture_time(self, start_time, end_time):
        # This function sets the times all lectures for this course
        for lecture in self.lectures:
            lecture.start_time = start_time
            lecture.end_time = end_time

    def last_prereq_day(self):
        # returns the day of the last prequsit for this course
        max_day = 0
        for course in self.prerequisites:
            if course.lectures[len(course.lectures) - 1].day > max_day:
                max_day = course.lectures[len(course.lectures) - 1].day
        return max_day

    def is_lab(self):
        return self.delivery == "Lab"

    def is_equal(self, other):
        if type(other) != Course:
            return False
        if len(self.prerequisites) != len(other.prerequisites):
            return False
        prereqs = zip(self.prerequisites, other.prerequisites)
        for prereq in prereqs:
            if not prereq[0].is_equal(prereq[1]):
                return False

        return self.name == other.name and self.total_hours == other.total_hours and self.hours_remaining == other.hours_remaining and self.delivery == other.delivery


    def __repr__(self):
        return self.name

    def create_empty_lectures(self):
        for i in range(0, self.number_of_lectures()):
            self.lectures.append(Lecture(0, 0, 0))

    def lecture_length(self):
        # Brian: not all stored lectures have a lecture length, not sure what to do when that happens
        extras = self.extra_req.split("|")
        lecture_length = 1.5
        for extra in extras:
            if extra.startswith("H"):
                lecture_length = float(extra.split("=")[1])


        return lecture_length

    def number_of_lectures(self):
        number_of_lectures = math.ceil(self.total_hours / self.lecture_length())
        return number_of_lectures

