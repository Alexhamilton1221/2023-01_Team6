
class Program:
    def __init__(self, name):
        # The name of the program (string)
        self.name = name
        # A list of stored courses, (array of Stored course object (!!!NOT Course!!!))
        self.stored_courses = []




    def add_course(self, stored_course):
        self.stored_courses.append(stored_course)

    def get_hours(self, specification=lambda course: True):
        # Gets the hours of a single term
        hours = 0
        for course in self.stored_courses:
            # Checks if the course is within the designed specification, default is always true
            if specification(course):
                hours += course.total_hours

        return hours

    def get_instance_courses(self, specification=lambda course: True):
        # Gets a list of courses in the format for usage (class type is course, not storedcourse)
        courses = []
        for course in self.stored_courses:
            # Checks if the course is within the designed specification, default is always true
            if specification(course):
                courses.append(course.generate_course())

                # This makes the prerequsite the actual same object
                for pre in courses[len(courses) - 1].prerequisites:
                    for matcher in courses:
                        if matcher.is_equal(pre):
                            courses[len(courses) - 1].prerequisites[courses[len(courses) - 1].prerequisites.index(pre)] = matcher
        return courses

    def is_core(self):
        # Returns whether this program is a core program
        return self.name == "PCOM" or self.name == "BCOM"

    #Other stuff
    def add_class(self, term, name, hours, islab=False):
        return
        #self.stored_courses[term].append("name" + "Hours")  # TODO -- create and append a "Class" object

    def __repr__(self) -> str:
        return self.name
        # Conlan: what is this? there is no term in stored_courses?
        # output = [self.name]
        #
        # for term in self.stored_courses:
        #     # ???
        #     for course in term:
        #         output.append(course.name)
        #
        # return str(output)

