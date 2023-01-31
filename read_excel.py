import pandas as pd

data = pd.read_excel("SCE_ProgramsCourses.xlsx")


print(data)




class Program:
    def __init__(self, name):

        self.name = name

        self.classes = [[],[],[]]

    def add_class(self, term, name, hours, islab=False):
        self.classes[term].append("name"+"Hours") # TODO -- create and append a "Class" object

    