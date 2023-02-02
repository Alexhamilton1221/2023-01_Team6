import pandas as pd
import openpyxl
import program
import classes

data = pd.read_excel("SCE_ProgramsCourses.xlsx")


#print(data)


wb = openpyxl.load_workbook("SCE_ProgramsCourses.xlsx")

# Get the first worksheet
ws = wb.worksheets[0]

lst = []

term = 1
r = 0
c = 0

for sheet in wb.worksheets:
    ws = sheet
    for row in ws.iter_rows():
        r += 1
        if r> 6: 
            print("--- Started Classes ---")
            cl = classes.Class("temp")
        for cell in row:
            c += 1
            if c > 5:
                continue
            if cell.value == "Term 1":
                term = 1
            elif cell.value == "Term 2":
                term = 2
            elif cell.value == "Term 3":
                term = 3
            elif "Total Term" in str(cell.value):
                break


            fill = cell.fill.start_color.rgb
            print(fill, ' - ', cell.value)
            if cell.value == "Class runs in a lab":
                lab_flag = fill
            elif cell.value == "Class runs in a lab and Classroom":
                hybrid_flag = fill
            elif cell.value == "Online only course":
                online_flag = fill

            if r > 6:
                if cell.value == None:
                    continue
                if c == 2:
                    cl.id = cell.value
                if c == 3:
                    cl.desc = cell.value
                if c == 4:
                    cl.hours = int(cell.value)
                cl.term = term

                if fill == lab_flag:
                    cl.type = "l"
                elif fill == hybrid_flag:
                    cl.type = "h"
                elif fill == online_flag:
                    cl.type = "o"
                else:
                    cl.type = "c"
        if r > 6 and cl.id != "temp":
            lst.append(cl)
        
        c = 0
        

    r = 0

for x in lst:
    print(str(x))