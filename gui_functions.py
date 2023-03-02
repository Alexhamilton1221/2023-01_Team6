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

