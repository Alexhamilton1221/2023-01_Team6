import openpyxl
from Database.program import Program
from Database.course import Course
from Database.classroom import Classroom
from Database.classrooms import Classrooms
from Database.cohort import Cohort
from Database.cohorts import Cohorts

import string


def get_color_code(ws):

    lab_flag = None
    hybrid_flag = None
    online_flag = None
    course_flag = None
    while not lab_flag and not hybrid_flag and not online_flag and not course_flag:
        for row in ws.iter_rows():
            for cell in row:

               

                if cell.value == "Class runs in a lab":
                    lab_flag = cell.fill.start_color.index
                elif cell.value == "Class runs in a lab and Classroom":
                    hybrid_flag = cell.fill.start_color.index
                elif cell.value == "Online only course":
                    online_flag = cell.fill.start_color.index
                elif cell.value == "Transcript Hours":
                    course_flag = cell.fill.start_color.index


    return [lab_flag, hybrid_flag, online_flag, course_flag]




def create_course(row, flags):
    lab_flag = flags[0]
    hybrid_flag = flags[1]
    online_flag = flags[2]
    #course_flag = flags[3]
    if row[1] == None or row[2] == None:
        return
    new_course = Course(row[1].value, 0, [])
    new_course.desc = row[2].value
    new_course.hours = row[3].value

    if row[1].fill == lab_flag:
        new_course.type = 'l'
    elif row[1].fill == online_flag:
        new_course.type = 'o'
    elif row[1].fill == hybrid_flag:
        new_course.type = 'h'

    return new_course


'''
Takes the cooridinate to the header of a program block in an excel file
Returns a Program object with Course objects loaded into it
'''
def create_program(sheet, header, flags):
    
    wb = openpyxl.load_workbook("SCE_ProgramsCourses.xlsx")

    # Get the first worksheet
    ws = sheet
    #program_name = ws[cords].value

    new_program = Program(header.value)

    term = 0
    courses = [[],[],[]]

    x = header.column
    #print(x)
    y = header.row
    
    for row in ws.iter_rows(min_row = y+1, min_col = x, max_col = x+4):
        #print('----\n', row[0].value, row[1].value, row[2].value, row[0].coordinate, '\n-----')
        if row[0].value != None:
   
            term += 1
     
        if row[1].value != None:

            new_course = create_course(row, flags)
            #print(courses, term)
            courses[term-1].append(new_course)


    new_program.courses = courses

    return new_program


#Returns the index of a letter in the alphabet
def char_position(letter):
    return ord(letter.lower()) - 97
    


def read_excel(filename):
    wb = openpyxl.load_workbook(filename)
    flags = get_color_code(wb.worksheets[0])

    
    programs = []
    #print(flags)
    for sheet in wb.worksheets:
        
        for row in sheet.iter_rows():
            for cell in row:
                if cell.fill.start_color.index == flags[-1] and cell.value != "Transcript Hours" and cell.value != "Pre-requisites":
                    #print(cell.value, 'TRIGGERED CREATE_PROGRAM')
                    new_program = create_program(sheet, cell, flags)
                    programs.append(new_program)

    return programs


#SCE_ProgramsCourses_(2023-02-01).xlsx

def get_classrooms(filename):
    ws = openpyxl.load_workbook(filename).worksheets[4]

    room_list = Classrooms()

    for row in ws.iter_rows(min_row=2):
        room_no = row[0].value.split(' ')[0]
        cap = int(row[1].value)
        new_classroom = Classroom(room_no, cap, ("lab" in row[0].value.lower()))
        room_list.add_classroom(new_classroom)

    return room_list


def get_registration(filename):

    ws = openpyxl.load_workbook(filename).worksheets[3]
    cohorts = Cohorts()

    for i in range(3):
        for row in ws.iter_rows(min_col=(i*2)+1, max_col=(i*2)+2, min_row=2):
            program_name = ""

            if row[0].value == None:
                continue

            for char in row[0].value:
                if not char.isnumeric():
                    program_name = program_name + char

            number = 1
            for o in cohorts.cohorts:
                if o.program == program_name and o.term == 0:
                    number += 1

            new_cohort = Cohort(program_name, 0, number, int(row[1].value), [])

            cohorts.add_cohort(new_cohort)
        
        for cohort in cohorts.cohorts:
            cohort.term += 1



    return cohorts

get_registration("SCE_ProgramsCourses_(2023-02-01).xlsx").show_cohorts()