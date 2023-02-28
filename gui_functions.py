import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import customtkinter
from tkinter import ttk, filedialog
from tkinter import messagebox
import datetime
#from datetime import datetime, timedelta

def import_excel(file_name,imp_type):
   global stud_file,res_file
   try:
       file = filedialog.askopenfile(mode='r', filetypes=[('CSV files', '*.xlsx')])
       f_name = os.path.basename(file.name)

       if file:
           file_name.configure(text=f_name)

       #Checks flag variable to update correct path
       if imp_type==1:
            stud_file=os.path.abspath(file.name)
       elif imp_type==2:
            res_file=os.path.abspath(file.name)
        
   except:
        messagebox.showwarning("Warning", "Failed to upload file.")


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
