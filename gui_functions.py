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
#from datetime import datetime, timedelta

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


# Takes list of entries from schedule page, time of class as a float, list of days as an index, length as a float
def create_schedule_block(entries_dict, time, days, length, name): #TODO SHOULD TAKE INDIVIDUAL LECTURES NOT PROGRAMS

    # Hard coded colors for each course TODO - ADD COLOR FOR EVERY COURSE *NOT* PROGRAM
    colors = {"BCOM": '#f4ceb8', 'PCOM': '#c2a2c2', 'BA': '#e9a7b8', 'DXD': '#d2ecff'}
    color = ""

    # Find color key in given name
    for key in colors:
        if key in name:
            color = colors[key]

    # Schedule begins at 8 so remove those indexes
    starting_hour = time - 8

    # Indexes in hour increments
    starting_hour = starting_hour // 0.5

    # For Each Coloumn
    for day in days:
        #For each entry in range of Length in half hour increments
        for hour in range(int(length/0.5)):

            # Get entry object at [Day_index, (starting_hour + each hour in length)]
            entry = entries_dict[(day,starting_hour+hour)]

            #Set color to course specific color
            entry.config(disabledbackground = color)
            entry.config(border=0)

            # Weird function to get course name and time printed in the middle of the block
            # Feel free to redo, idek what i was thinking
            display_time = time
            if time > 12:
                display_time = time-12
            display_time = f"{display_time}  -  {display_time+length}"

            if hour == int(length)-1:
                entry.config(state=NORMAL)
                entry.insert(0,name)
                entry.config(state=DISABLED)

            if hour == int(length):
                entry.config(state=NORMAL)
                entry.insert(0,display_time)
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

    for spn in spinner_object: #Error Checking
        #print('test',int(spn.get()))
        if int(spn.get())>100:
            messagebox.showerror("Error", "You entered too many Students. \nA maximum of 100 students is permitted.")
            spn.set(0)
            return
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
        print(row_num)
        row_num+=1

    print("break")

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
        
        print(row_num)
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