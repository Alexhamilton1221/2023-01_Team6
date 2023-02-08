
class Program:
    def __init__(self, name):
        # The name of the program
        self.name = name
        # A list of stored courses,
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
        return courses

    def is_core(self):
        # Returns whether this program is a core program
        return self.name == "PCOM" or self.name == "BCOM"

    #Other stuff
    def add_class(self, term, name, hours, islab=False):
        self.courses[term].append("name" + "Hours")  # TODO -- create and append a "Class" object

    def __repr__(self) -> str:
        output = [self.name]

        for term in self.courses:
            for course in term:
                output.append(course.name)

        return str(output)

