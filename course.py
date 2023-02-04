

class Course:
    def __init__(self, id):
        self.id = id
        self.desc = ""
        self.hours = 0
        self.room = ""
        self.type = ""
        self.term = 0


    def __str__(self):

        return str([self.id, self.desc, self.hours, self.term, self.type])
        