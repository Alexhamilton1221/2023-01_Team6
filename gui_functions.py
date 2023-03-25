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

import random
from Database.cohorts import Cohorts
from Database.programs import Programs
from hardCodedClassrooms import temp_Classroom_add
from hardCodedCourses import temp_create_courses
#from datetime import datetime, timedelta

# Global Vars for preventing multiple windows opening
new_window_open = False
new_window = None


def import_excel(file_name,imp_type, spn=None):
   global stud_file,res_file
   try:
       file = filedialog.askopenfile(mode='r', filetypes=[('CSV files', '*.xlsx')])
       f_name = os.path.basename(file.name)

       if file:
           file_name.configure(text=f_name)

       #Checks flag variable to update correct path
       if imp_type==1:
            stud_file=os.path.abspath(file.name)
            registration = get_registration(stud_file)

            update_spinners(registration, spn)

            # TEMP FUNCTION TO RUN ON EXECUTE
            # Assumes term is spring
            reg_list = []
            #for key in registration.keys():
            #    if registration.get(key) > 0:
            #        reg_list.append([key, registration.get(key)])

            #cohorts = Cohorts()
            #programs = Programs(temp_create_courses())
            #classrooms = Classrooms(temp_Classroom_add())
            #cohorts.create_cohorts(classrooms, programs, reg_list)
            #cohorts.create_schedules(1)
            #cohorts.cohorts[0]
       elif imp_type==2:
            res_file=os.path.abspath(file.name)
        
   except Exception as e:
        messagebox.showwarning("Warning", "Failed to upload file. " + str(e))


#This function forms the schedule. It takes the 2 names of each excel file
#names as parameters.
def form_schedule(student_list_name,resouce_list_name):
    global stud_file,res_file #These are the complete paths to the 2 excel files

    print('Creating Schedule')
 
    #If the schedule creation is successfull show successful message.
    #messagebox.showinfo("Note", "Successfully formed a Schedule")

#Function for downloading scedule, maybe need this
def save_schedule():
    print('Downloading Schedule')
    messagebox.showinfo("Note", "Successfully downloaded the Schedule")

#Form the schedule when optionbox is changed
# def form_schedule_screen(frame_t2_background):
   
#     times =["6:00 am", "6:30 am", "7:00 am", "7:30 am", "8:00 am", "8:30 am",
#              "9:00 am", "9:30 am", "10:00 am", "10:30 am", "11:00 am",
#              "11:30 am",
#              "12:00 pm", "12:30 pm", "1:00 pm", "1:30 pm", "2:00 pm", "2:30 pm",
#              "3:00 pm", "3:30 pm",
#              "4:00 pm", "4:30 pm", "5:00 pm", "5:30 pm", "6:00 pm", "6:30 pm",
#              "7:00 pm"]
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
    
#     print()
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
        course = key.split(" ")[0]
        term = key.split(" ")[1]
        num = registration[key]

        # Reconstruct data into format used in spinner creation
        spn_name = "spn_" + course.lower() + '_t' + str(term)
        
        
        #Change the var at the same index as the formatted key in the list of spinners
        vars[spn_names.index(spn_name)].set(str(num))
       



# Parse registration numbers from excel file
# Takes a file name of the excel file
# Returns a dictionary formatted: "{Corse_Name} {Term}": int(Registration_Amount) 
def get_registration(filename):

     #Open excel file 
    try:
        sheet = openpyxl.load_workbook(filename).worksheets[0]

    except:
        #Error opening file, return None
        return None
    
    # Init return object
    registration = {}

    # For each row in the excel file, skipping the header
    for row in sheet.iter_rows(min_row=2):
        if row[0].value == None:
            continue

        #Index of values unsure - template not uploaded yet
        course = row[1].value 
        term = row[0].value 
        num = row[2].value

        registration[course + " " + str(term)] = int(num)


    return registration


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

#Takes a time and converts it to its regular time 
def conv_time(start_time,end_time):
     # Init display variable
    display_time = start_time
    display_time_end = end_time
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
        
    return display_time,display_time_end

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

    # Indexes in half hour increments so double the starting hour
    starting_index = starting_hour // 0.5

    # Get day in terms of index of week, lectures start at 1, indexs at 0 so -1
    day = (lecture.day % 4)-1
    # If wrapped around, 
    if day == -1:
        day = 3

    length =  lecture.end_time - lecture.start_time
    
    display_time,display_time_end=conv_time(lecture.start_time,lecture.end_time)

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
            entry.insert(0, name + ' - ' + cohort.name)
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
    for cohort in classrooms.classrooms[2].cohorts:
        for course in cohort.courses:
            for lecture in course.lectures:
                if lecture.day < 12:
                    print(classrooms.classrooms[2].name, ' - ', course.name, lecture.day, lecture.start_time, course.delivery)
                    
                    
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

                        
                        #print("TESTING",display_time)    
                        if len(display_time)==6:
                            #print("HERE"+ display_time)
                            display_time=f"0{display_time} "
                        
                        #print(classrooms.classrooms[i].name, ' - ', course.name, lecture.day, lecture.start_time, course.delivery)
                        #For testing include classroom name but remove later
                        text_field.insert(tk.END,classrooms.classrooms[i].name+ ' - ' +course.name+' - Days: '+str(lecture.day)+str(days_spacing)+
                        '      Start Time: '+str(display_time) +'      Delivery Type: '+ course.delivery+'\n')
                        
    text_field.configure(state='disabled')
        
class Calendar(tk.Frame):
    def __init__(self, parent,array_rect,array_lbl,semester_lectures):
        tk.Frame.__init__(self, parent)
        # Create Array for all Rectangles
        # When rectangles are saved to array, they are saved by an ID number
        # Must reference them using methods.
        self.array_rect=array_rect
        self.array_lbl=array_lbl
        self.semester_lectures=semester_lectures
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
    
    def close_new_window(self):
        global new_window_open
        # Set the new window flag to False and destroy the window
        new_window_open = False
        new_window.destroy()
        
    
    def clean_array(self):
        while self.semester_lectures:
            self.semester_lectures.pop()

    #def clean_array(self):
     #   self.semester_lectures = [subarr for subarr in self.semester_lectures if subarr]
    
    
    def calendar_entry_clicked(self,event,row,col):
        global new_window_open, new_window
        
        new_window_body=("Arial", 14) 

        #Number of columns
        num_of_columns=7
        index=  row *num_of_columns  + col

        # Create New Window Displaying Class Info
        # TODO Make the title the appropriate date
        if not new_window_open:
            #Create New Window
            new_window = tk.Toplevel(self.canvas)
            new_window.title("Date {class_etr[0]}") 
            new_window.geometry("640x360")
            new_window.config(background='#252526')
            
            #Call Class to construct Canvas
            entry_frame = Day(new_window)
            entry_frame.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.9, anchor='n')    
            
            indexed_lecs=[]
            for subarr in self.semester_lectures:
                if subarr[0]==index:
                    indexed_lecs.append(subarr)
                    #print('new',subarr)

            sorted_list = sorted(indexed_lecs, key=lambda x: x[5])
            
            #For Testing
            #TODO Place Date in this Object Using for testing
            title = tk.Label(new_window, text=f"Date {sorted_list[0][0]}", bg="#252526", fg='white',font=new_window_body)
            title.pack()


            
            x1=325 ; y1=20 ; pad_y=0
            for class_etr in sorted_list:
                new_text=f" {class_etr[1]} {class_etr[2]} {class_etr[3]} - {class_etr[4]}"
                
                entry_frame.canvas.create_text(x1,y1+pad_y,text=new_text,fill="white",font=new_window_body)
                #self.canvas.itemconfigure(text, fill="blue")

                pad_y+=20
                  

            #Screen Settings
            
            # Make it so that window cannot change size/shape
            new_window.attributes('-fullscreen', False)
            new_window.resizable(False, False)

            #Call function to close window to prevent multiple open windows
            new_window_open = True
            new_window.protocol("WM_DELETE_WINDOW", self.close_new_window)

    
    
    def setup_grid(self):
        rect_size = 180
        count=0
        for row in range(5):
            for col in range(7):
                x1 = col * rect_size
                y1 = row * rect_size
                x2 = x1 + rect_size
                y2 = y1 + rect_size
                rect=self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='white')
                self.canvas.tag_bind(count+1, "<Button-1>", lambda event, row=row, col=col: self.calendar_entry_clicked(event,row, col))

                #self.canvas.tag_bind(rect, "<Button-1>", lambda event, index=count: self.on_rectangle_click())
                #self.canvas.tag_bind(rect, "<Button-1>", self.calendar_entry_clicked)

                self.array_rect.append(rect)
                count+=1

        #Deal With last Entry
        self.canvas.tag_bind(count+1, "<Button-1>", lambda event, row=row, col=col: self.calendar_entry_clicked(event,row, col+1))

        #print(self.array_rect)
        
    def clear_grid(self):
        text_items = self.canvas.find_all()     
        for item in text_items:
            if self.canvas.type(item) == "text":
                self.canvas.delete(item)


    def calendar_day_entry(self,sorted_list,i):
        count=0; rect_size = 180
                
        # Font for Calendar Creation
        my_font = ("Arial", 24) 

        for row in range(5):
            for col in range(7):
                count+=1
                pad_y=0
                
                # Default Case: Print all Lectures
                if count==i and len(sorted_list)<8:
                    x1 = col * rect_size; x1+=85
                    y1 = row * rect_size+pad_y; y1+=15; 

                    for cal_etr in sorted_list:
                        new_text=f" {cal_etr[1]} {cal_etr[2]}"

                        text = self.canvas.create_text(x1,y1+pad_y,text=new_text)
                        
                        self.array_lbl.append(text)
                        pad_y+=15
                
                # Second Case: Print 8 lectures and add ...
                elif count==i: 
                    x1 = col * rect_size; x1+=85
                    y1 = row * rect_size+pad_y; y1+=15; 

                    for cal_etr in sorted_list[:8]:
                        new_text=f" {cal_etr[1]} {cal_etr[2]}"

                        text = self.canvas.create_text(x1,y1+pad_y,text=new_text)
                        self.array_lbl.append(text)
                        pad_y+=15
                    text = self.canvas.create_text(x1,y1+pad_y,text="...", font=my_font)
        #self.semester_lectures.append(sorted_list)
        
        


class Day(tk.Frame):
    def __init__(self, parent,):
        tk.Frame.__init__(self, parent)
        
        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        # Create a canvas to contain the widgets
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=scrollbar.set,background='#3e3e42')
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
