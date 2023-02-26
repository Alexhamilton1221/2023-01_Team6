import openpyxl
from Database.program import Program
from Database.course import Course
from Database.classroom import Classroom
from Database.classrooms import Classrooms
from Database.cohort import Cohort
from Database.cohorts import Cohorts

import string

'''
Takes a file name refrencing program information excel file
Returns a Classrooms object containing a list of Classroom objects for each classroom
'''
def get_classrooms(filename):

    #Init excel work sheet
    ws = openpyxl.load_workbook(filename).worksheets[4]

    #Object to hold each Classroom
    room_list = Classrooms()

    #For each classroom row, skipping the header
    for row in ws.iter_rows(min_row=2):
        #Sterilize room No. info
        room_no = row[0].value.split(' ')[0]
        #Save capacity as an int
        cap = int(row[1].value)
        #Create Classroom object
        new_classroom = Classroom(room_no, cap, ("lab" in row[0].value.lower()))
        #Add to Classrooms List
        room_list.add_classroom(new_classroom)

    #Return entire list
    return room_list



def get_registration(filename):

     #Open excel file and init return object
    sheet = openpyxl.load_workbook(filename).worksheets[3]

    registration = {}

    for row in sheet.iter_rows():
        if row[0].value == None:
            continue

        #Idex of values unsure - template not uploaded yet
        course = row[0].value 
        term = row[1].value
        num = row[2].value

        registration[course + " " + term] = int(num)


    return registration






#Returns the index of a letter in the alphabet
def char_position(letter):
    return ord(letter.lower()) - 97
    



'''        Redundant, commented for posterity

Takes a file name refrencing the program information excel sheet
Returns a Cohorts object populated with the Cohorts for the previous 3 terms

def get_registration(filename):

    #Open excel file and init return object
    ws = openpyxl.load_workbook(filename).worksheets[3]
    cohorts = Cohorts()

    #For each term of cohorts required
    for i in range(3):
        #For each row containing a cohort and its registration amount
        for row in ws.iter_rows(min_col=(i*2)+1, max_col=(i*2)+2, min_row=2): #Just 2 cols for each term, skipping header
            program_name = ""

            #If empty row, skip
            if row[0].value == None:
                continue

            #Get just letters in cohort program - input sterilization
            for char in row[0].value:
                if not char.isnumeric():
                    program_name = program_name + char

            #Count already created cohorts with same program name to get id number for cohort
            number = 1
            for o in cohorts.cohorts:
                if o.program == program_name and o.term == 0:
                    number += 1

            #Create new cohort object -- TODO add actual couse information
            new_cohort = Cohort(program_name, 0, number, int(row[1].value), [])

            #Add to cohorts object
            cohorts.add_cohort(new_cohort)
        
        #Increment term for all cohorts, continue to next terms registration numbers
        for cohort in cohorts.cohorts:
            cohort.term += 1


    #Return object containing all cohorts
    return cohorts

get_registration("SCE_ProgramsCourses_(2023-02-01).xlsx").show_cohorts()
'''


