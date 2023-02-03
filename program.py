
class Program:
    def __init__(self, name):

        self.name = name

        self.courses = [[],[],[]]

    def add_class(self, term, name, hours, islab=False):
        self.courses[term].append("name"+"Hours") # TODO -- create and append a "Class" object

    def __repr__(self) -> str:
        output = [self.name]
        
        for term in self.courses:
            for course in term:
                output.append(course.id)

        return str(output)