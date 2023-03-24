import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import customtkinter
from tkinter import ttk, filedialog
from tkinter import messagebox
import datetime
import openpyxl
from Database.classrooms import Classrooms
from Database.classroom import Classroom
from Database.students import Students
from Database.student import Student
import random
from Database.cohorts import Cohorts
from Database.programs import Programs
from hardCodedClassrooms import temp_Classroom_add
from hardCodedCourses import temp_create_courses
#import main as m




#from datetime import datetime, timedelta

#This is for Calendar Creation
global lbl_x,lbl_y
global reg_numbers 
reg_numbers= []
global student_info

reg_numbers = None
student_info = None
lbl_x=50; lbl_y=20

def import_excel(file_name,imp_type, spn=None):
   global stud_file,res_file
   try:
       file = filedialog.askopenfile(mode='r', filetypes=[('CSV files', '*.xlsx')])
       f_name = os.path.basename(file.name)

       #if file:
           #file_name.configure(text=f_name)

       #Checks flag variable to update correct path
       if imp_type==1:
            stud_file=os.path.abspath(file.name)
            registration, student_list = get_registration(stud_file)

            update_spinners(registration, spn)

      
       elif imp_type==2:
            res_file=os.path.abspath(file.name)
            return get_classrooms(file.name)
        
   except Exception as e:
        messagebox.showwarning("Warning", "Failed to upload file. " + str(e))


#This function forms the schedule. It takes the 2 names of each excel file
#names as parameters.
def form_schedule(classroom_list, total_lables, var_chosen_term):
    global stud_file,res_file #These are the complete paths to the 2 excel files
    global reg_numbers, student_info

    cur_semester = 1
    if var_chosen_term.get() == "Fall":
        cur_semester = 1
    elif var_chosen_term.get() == "Winter":
        cur_semester = 2
    elif var_chosen_term.get() == "Spring/Summer":
        cur_semester = 3


    total_order = ['PCOM', 'BCOM', "PM", "BA", "GLM", "FS", "DXD", "BK"]
    


    programs = Programs(temp_create_courses())
    classrooms = Classrooms(classroom_list)
    students = reg_numbers
    print(students)

    has_made_schedule = False
    time_mod = 1.0
    cohorts = Cohorts()

    while has_made_schedule == False:
        try:
            has_made_schedule = True
            cohorts.cohorts = []
            cohorts.create_cohorts(classrooms, programs, students, 2, time_mod)
            cohorts.create_schedules(2)
        except ValueError:
            has_made_schedule = False
            time_mod += 0.1

    print_schedule(classrooms)
    student_info.add_to_cohorts(programs, cohorts)
    for room in classrooms.get_rooms():
        room.check_for_conflict()

 
    #If the schedule creation is successfull show successful message.
    #messagebox.showinfo("Note", "Successfully formed a Schedule")

#Function for downloading scedule, maybe need this
def save_schedule():
    print('Downloading Schedule')
    messagebox.showinfo("Note", "Successfully downloaded the Schedule")

#Form the schedule when optionbox is changed
def form_schedule_screen(frame_t2_background):
   
    times =["6:00 am", "6:30 am", "7:00 am", "7:30 am", "8:00 am", "8:30 am",
             "9:00 am", "9:30 am", "10:00 am", "10:30 am", "11:00 am",
             "11:30 am",
             "12:00 pm", "12:30 pm", "1:00 pm", "1:30 pm", "2:00 pm", "2:30 pm",
             "3:00 pm", "3:30 pm",
             "4:00 pm", "4:30 pm", "5:00 pm", "5:30 pm", "6:00 pm", "6:30 pm",
             "7:00 pm"]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
    
    print()
     # Horizontal lines serparating times
    #for i in days:
    #frame_t2_background.create_line(50, 0, 50, 20, fill="red", width=2)



# Updates spinners on main screen when excel file is imported
# Takes list of registration numbers from get_registration() and a list containing the spinner names and the corresponding vars
def update_spinners(registration, spn):

    # Extract spinner keys and vars
    spn_names = spn[0]
    vars = spn[1]

    for key in registration:
        # extract data from registration numbers
        course = key[0].split(" ")[0]
        term = key[0].split(" ")[1]
        num = key[1]

        # Reconstruct data into format used in spinner creation
        spn_name = "spn_" + course.lower() + '_t' + str(term)
        
        
        #Change the var at the same index as the formatted key in the list of spinners
        vars[spn_names.index(spn_name)].set(str(0))
        vars[spn_names.index(spn_name)].set(str(num))
       



# Parse registration numbers from excel file
# Takes a file name of the excel file
# Returns a dictionary formatted: "{Corse_Name} {Term}": int(Registration_Amount) 
def get_registration(filename):
    global reg_numbers, student_info
     #Open excel file 
    try:
        sheet = openpyxl.load_workbook(filename).worksheets[0]

    except:
        #Error opening file, return None
        return None
    
    student_list = Students()
    registration = {}

    # Check format for registration file
    if sheet['a1'].value == 'Id':
        # STUDENT INFORMATION
        

        for row in sheet.iter_rows(min_row=2):
            new_student = Student(id= row[0].value,name=row[1].value, term=row[2].value, 
                                  core=row[3].value, program=row[4].value)
            
            
            student_list.students.append(new_student)

        # Sum core and noncore registration numbers
        for student in student_list.students:
            core_key = str(student.core) + ' ' + str(student.term)
            noncore_key = str(student.program) + ' ' + str(student.term)


            # Increment counter for registration for both core and noncore program
            if core_key in registration.keys():
                registration[core_key] += 1
            else:
                registration[core_key] = 1

            if noncore_key in registration.keys():
                registration[noncore_key] += 1
            else:
                registration[noncore_key] = 1


    else: # Just registration info

        # For each row in the excel file, skipping the header
        for row in sheet.iter_rows(min_row=2):
            if row[0].value == None:
                continue

            course = row[1].value 
            term = row[0].value 
            num = row[2].value

            if num == 0 or num == None:
                continue

            registration[course + " " + str(term)] = int(num)



        temp = registration.copy()
        student_id = -1

        for i in temp.keys():
            course = i.split(' ')[0]
            term = i.split(' ')[1]


            # If not a core registration
            if 'PCOM' not in course and 'BCOM' not in course:
                continue
            

            for p in range(temp[i]):
                # Find a noncore reg of the same term to match with
                for o in temp:
                    course_2 = o.split(' ')[0]
                    term_2 = o.split(' ')[0]

                    # If this is a core or is of wrong term, continue
                    if 'PCOM' in o or 'BCOM' in o or i[-1] != o[-1] or temp[o] == 0:
                        continue
                    #if term != term_2 or 'PCOM' in course or 'BCOM' in course or temp[o] == 0:
                        
                    
                    new_student = Student(id=student_id, name="FakeName", term=term, core=course, program=course_2)
                    student_list.students.append(new_student)

                    temp[o] -= 1
                    temp[i] = temp[i]-1
                    student_id -= 1

                    break




    #Turn dictionary into a list of lists
    reg_list = []
    for key in registration:
        reg_list.append([key, registration[key]])

    reg_numbers = reg_list
    student_info = student_list
    return (reg_list, student_list)




def create_student_objects(reg_numbers):
    pass



'''
Takes a file name refrencing program information excel file
Returns a Classrooms object containing a list of Classroom objects for each classroom
'''
def get_classrooms(filename):

    #Init excel work sheet
    ws = openpyxl.load_workbook(filename).worksheets[-1]

    #Object to hold each Classroom
    room_list = Classrooms()

    #For each classroom row, skipping the header
    for row in ws.iter_rows(min_row=2):
        if row[0].value == None:
            continue

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


# Takes list of entries from schedule page, time of class as a float, list of days as an index, length as a float
def create_schedule_block(entries_dict, lecture, name, cohort): 

    program = cohort.program.name

    colors = {"BCOM": '#f4ceb8', 'PCOM': '#c2a2c2', 'BA': '#e9a7b8', 'DXD': '#a7bed3',
              'PM': '#00A5E3', 'FS': '#8dd7bf', 'GLM': '#00cdac', 'BK': '#6c88c4'}
    color = ''
    for key in colors.keys():
        if program in key:
            color = colors[key]
    if len(color) == 0:
        r = lambda: random.randint(0,255)
        color = '#%02X%02X%02X' % (r(),r(),r())


    # Schedule begins at 8 so remove those indexes
    starting_hour = lecture.start_time - 8

    # Indexes in hlaf hour increments so double the starting hour
    starting_index = starting_hour // 0.5

    # Get day in terms of index of week, lectures start at 1, indexs at 0 so -1
    day = (lecture.day % 4)-1
    # If wrapped around, 
    if day == -1:
        day = 3

    length =  lecture.end_time - lecture.start_time

    #print(name, lecture.start_time, lecture.day, length)

    # Init display variable
    display_time = lecture.start_time
    display_time_end = lecture.end_time
    start_pm = False; end_pm = False

    # If time is greater than 12, keep in 12hr format
    if display_time > 12:
        display_time -= 12
        start_pm = True
    if display_time_end > 12:
        display_time_end -= 12
        end_pm = True

    # If start or end time is a half hour,  
    if display_time.is_integer():
        display_time = f"{int(display_time)}:00"
    else:
        display_time = f"{int(display_time)}:30"

    if start_pm:
        display_time += "pm"
    else:
        display_time += "am"

    if display_time_end.is_integer():
        display_time_end = f"{int(display_time_end)}:00"
    else:
        display_time_end = f"{int(display_time_end)}:30"

    if end_pm:
        display_time_end += "pm"
    else:
        display_time_end += "am"


    #For each entry in range of Length in half hour increments
    for hour in range(int(length/0.5)):

        # Get entry object at [Day_index, (starting_hour + each hour in length)]
        entry = entries_dict[(day, starting_index+hour)]

        #Set color to course specific color
        entry.config(disabledbackground = color)
        #entry.config(borderwidth=0)
        #entry.config()

        # Weird function to get course name and time printed in the middle of the block
        # Feel free to redo, idek what i was thinking
        
        
        if hour == int(length)-1:
            entry.config(state=NORMAL)
            entry.insert(0, cohort.name + ' - ' + name)
            entry.config(state=DISABLED)

        if hour == int(length):
            entry.config(state=NORMAL)
            entry.insert(0,f"{display_time} - {display_time_end}")
            entry.config(state=DISABLED)


# Function for when a new term is selected from dropdown.
# Takes the term chosen from dropdown and label lists and updates title labels
def term_changed(var_chosenterm,infolabelscore,infolabelsnoncore):
    termlist=["Fall","Winter","Spring/Summer"]
    term=var_chosenterm.get()
    if term=="Fall":
        for i in range(1, 4):
            infolabelscore[i].configure(text=termlist[i-1])
            infolabelsnoncore[i-1].configure(text=termlist[i-1])
            
    elif term=="Winter":
        for i in range(1, 3):
            infolabelscore[i].configure(text=termlist[i])
            infolabelsnoncore[i-1].configure(text=termlist[i])
        
        infolabelscore[3].configure(text=termlist[0])
        infolabelsnoncore[2].configure(text=termlist[0])
   
    else:
        infolabelscore[1].configure(text=termlist[2])
        infolabelsnoncore[0].configure(text=termlist[2])
        
        for i in range(3, 1,-1):
                infolabelscore[i].configure(text=termlist[i-2])
                infolabelsnoncore[i-1].configure(text=termlist[i-2])
        
# This function is called whenever a Spinbox is updated to print the new totals.
def update_totals(spinners,total_labels,row_num,spinner_object):

    all_programs=['pcom','bcom','pm','ba','gl','fs','dxd','bk']
    sum=0
    if row_num==1:
        substring = 'pcom'
    elif row_num==2:
        substring = 'bcom'
    elif row_num==3:
        substring = 'pm'
    elif row_num==4:
        substring = 'ba'    
    elif row_num==5:
        substring = 'gl'    
    elif row_num==6:
        substring = 'fs'    
    elif row_num==7:
        substring = 'dxd'    
    elif row_num==8:
        substring = 'bk'    
    
    for spn in spinner_object: #Error Checking
        #print('test',int(spn.get()))
        if int(spn.get())>100:
            messagebox.showerror("Error", "You entered too many Students. \nA maximum of 100 students is permitted.")
            spn.set(0)
            indices = [i for i, s in enumerate(spinners) if substring in s]
            total_labels[row_num-1].configure(text=0)
            for i in indices:
                text=int(spinner_object[i].get())+total_labels[row_num-1].cget("text")
                #print(type(sum))
                sum+=text
                #print(sum)
            total_labels[row_num-1].configure(text=sum)            
            return
    
    indices = [i for i, s in enumerate(spinners) if substring in s]
      
    total_labels[row_num-1].configure(text=0)

    for i in indices:
        text=int(spinner_object[i].get())+total_labels[row_num-1].cget("text")
            
        total_labels[row_num-1].configure(text=text)

# This function is called when somebody types in a value. Need to check all spinboxes.
def update_all_totals(spn_core,spn_noncore,total_labels,spinner_object):
    #programs=['pcom','bcom','pm','ba','gl','fs','dxd','bk']
    core_programs=['pcom','bcom']; non_core_programs=['pm','ba','gl','fs','dxd','bk']
    row_num=1
    
    
    
    for core_substring in core_programs:
        
        core_indices = [i for i, s in enumerate(spn_core) if core_substring in s]
        
        #print(core_indices)

        total_labels[row_num-1].configure(text=0)
        for i in core_indices:
            text=int(spinner_object[i].get())+total_labels[row_num-1].cget("text")
                
            total_labels[row_num-1].configure(text=text)
        #print(row_num)
        row_num+=1



        
    #print("break")

    #row_num=1
    for non_core_substring in non_core_programs:
        #print(non_core_substring)

        non_core_indices = [j for j, k in enumerate(spn_noncore) if non_core_substring in k]
        
        for i in range(len(non_core_indices)): #Deal with new list by adding 6
            non_core_indices[i] += 6
        
        #print(non_core_indices)

        total_labels[row_num-1].configure(text=0)

        for j in non_core_indices:
            text=int(spinner_object[j].get())+total_labels[row_num-1].cget("text")
                
            total_labels[row_num-1].configure(text=text)
        
        #print(row_num)
        row_num+=1
    
    # full_spn=spn_core.update(spn_noncore)
    # print('HERE',type(spn_core))
    # print(spn_core)
    # print(spn_noncore)

    # print('HERE',type(full_spn))
    # for substring in programs:
    
    #     indices = [i for i, s in enumerate(full_spn) if substring in s]
      
    #     total_labels[row_num-1].configure(text=0)

    #     for i in indices:
    #         text=int(spinner_object[i].get())+total_labels[row_num-1].cget("text")
            
    #         total_labels[row_num-1].configure(text=text)

        
def change_classroom(label, var):
    data = var.get()
    label.configure(text=str(data))
   
   
   
# #Get current Season for Term
# def get_season():
#     now = datetime.datetime.now()
#     if now.month >= 9 and now.month <= 12:
#         return "Fall"
#     elif now.month >= 6 and now.month <= 8:
    
#     else:
#         return "Winter"   
#     # if now.month >= 3 and now.month <= 5:
#     #     return "Spring"
#     # elif now.month >= 6 and now.month <= 8:
#     #     return "Summer"
#     # elif now.month >= 9 and now.month <= 11:
#     #     return "Fall"
#     # else:
#     #     return "Winter"   
# def on_enter(event):
#     event.widget.config(bg="#3e3e42")

# def on_leave(event):
#     event.widget.config(bg="#252526")


def clear_schedule(entries):
    for index in entries:
        entries[index].config(state=NORMAL)
        entries[index].delete(0, END)
        entries[index].config(disabledbackground = '#ffffff')
        entries[index].config(state=DISABLED)

#prints total schedule for a room
def print_schedule(classrooms):
    #for room in classrooms:
    for room in classrooms.classrooms:
        for cohort in room.cohorts:
            for course in cohort.courses:
                for lecture in course.lectures:
                    if lecture.day < 12:
                        print(room.name, ' - ', course.name, lecture.day, lecture.start_time, course.delivery)
                        
                        
def print_cohorts(classrooms,cohort_name,text_field):
    #print('###################################################################################################')
    #print('###################################################################################################')
    #print('TEST',cohort_name)
    #Testing Print
    text_field.configure(state='normal')

    text_field.delete("1.0", "end") #Clear Text Field
    for i,x in enumerate(classrooms.classrooms):
        for cohort in classrooms.classrooms[3].cohorts:
            for course in cohort.courses:
                if classrooms.classrooms[i].name==cohort_name:
                    for lecture in course.lectures:
                        #Fixing Indentation
                        if lecture.day<10:
                            days_spacing="   -"
                        elif lecture.day<99:
                            days_spacing=" -"
                        else:
                            days_spacing="-"

                        #Init display variable
                        display_time = lecture.start_time
                        display_time_end = lecture.end_time
                        start_pm = False; end_pm = False

                        # If time is greater than 12, keep in 12hr format
                        if display_time > 12:
                            display_time -= 12
                            start_pm = True
                        if display_time_end > 12:
                            display_time_end -= 12
                            end_pm = True

                        # If start or end time is a half hour,  
                        if display_time.is_integer():
                            display_time = f"{int(display_time)}:00"
                        else:
                            display_time = f"{int(display_time)}:30"

                        if start_pm:
                            display_time += "pm"
                        else:
                            display_time += "am"

                        if display_time_end.is_integer():
                            display_time_end = f"{int(display_time_end)}:00"
                        else:
                            display_time_end = f"{int(display_time_end)}:30"

                        if end_pm:
                            display_time_end += "pm"
                        else:
                            display_time_end += "am"

                        
                        #print("TESTING",len(display_time))    
                        if len(display_time)==6:
                            #print("HERE"+ display_time)
                            display_time=f"0{display_time} "
                        
                        #print(classrooms.classrooms[i].name, ' - ', course.name, lecture.day, lecture.start_time, course.delivery)
                        #For testing include classroom name but remove later
                        text_field.insert(tk.END,classrooms.classrooms[i].name+ ' - ' +course.name+' - Days: '+str(lecture.day)+str(days_spacing)+
                        '      Start Time: '+str(display_time) +'      Delivery Type: '+ course.delivery+'\n')
                        
    text_field.configure(state='disabled')



        
class ScrollableFrame(tk.Frame):
    def __init__(self, parent,array_rect,array_lbl):
        tk.Frame.__init__(self, parent)
    #Create Array for all Rectangles
        self.array_rect=array_rect
        self.array_lbl=array_lbl

        
        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        # Create a canvas to contain the widgets
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=canvas.yview)

        # Set the canvas to expand to fill the entire frame
        self.canvas = canvas
        canvas.bind('<Configure>', self._configure_canvas)

        # Create a frame to hold the widgets
        self.inner_frame = tk.Frame(canvas)
        self.inner_frame_id = canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        # Hide the canvas
        canvas.configure(borderwidth=0, highlightthickness=0)
        
        
        
    def _configure_canvas(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def update_viewport(self):
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
     
    def setup_grid(self):
        rect_size = 180
        for row in range(9):
            for col in range(7):
                x1 = col * rect_size
                y1 = row * rect_size
                x2 = x1 + rect_size
                y2 = y1 + rect_size
                rect=self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='white')
                self.array_rect.append(rect)

    def clear_grid(self):
        text_items = self.canvas.find_all()
        for item in text_items:
            if self.canvas.type(item) == "text":
                self.canvas.delete(item)


    def formrect(self,sorted_list,i):
        #print(sorted_list)
        count=0
        rect_size = 180
        for row in range(9):
            for col in range(7):
                count+=1
                pad_y=0
                if count==i:
                    x1 = col * rect_size; x1+=85
                    y1 = row * rect_size+pad_y; y1+=15; 

                    #rect=self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='white')
                    for j in sorted_list:
                        text = self.canvas.create_text(x1,y1+pad_y,text=j)
                        self.array_lbl.append(text)
                        pad_y+=15

        #print(self.array_lbl)




        # area_x = -490
        # area_y = 0
        
        # padding_y=20

        
        # for j in sorted_list:
        #     current=self.array_rect[i]
        #     print('test',current)
        #     text_x = area_x+185*current
        #     text_y = (area_y*current)+padding_y
        #     text = self.canvas.create_text(text_x,text_y,text=j)
        #     print(j)
            
        #     padding_y+=15

            
            #lbl_y+=15

        # lbl_x+=100
        #lbl_y+=20