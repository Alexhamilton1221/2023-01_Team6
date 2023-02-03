import pandas as pd
import openpyxl
import program
import course
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
    new_course = course.Course(row[1].value)
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

    new_program = program.Program(header.value)

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


programs = read_excel("SCE_ProgramsCourses.xlsx")



for prog in programs:
    print(prog)