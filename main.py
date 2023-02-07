#modules
import os
import tkinter as tk
import customtkinter
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas as pd
import openpyxl
from Database.classroom import Classroom


#Global variables for 2 excel paths
stud_file=''
res_file=''

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
    
    '''
    Error checking, keep commented for testing. Don't remove
    

    # if len(student_list_name)==0 and len(resouce_list_name)==0:
    #         messagebox.showinfo("Warning", "Missing both excel files")
    #         return
    # elif len(student_list_name)==0:
    #         messagebox.showinfo("Warning", "Missing Student List Excel File")
    #         return
    # elif len(resouce_list_name)==0:
    #         messagebox.showinfo("Warning", "Missing Class Resource List Excel File")
    #         return
    '''
    
    #print("TEST STUD:"+stud_file)
    #print("TEST RES:"+res_file)
    print("TEST STUD:"+student_list_name)
    print("TEST RES:"+resouce_list_name)
    '''
    Testing with openpyxl can delete this

    #df = pd.read_excel(stud_file) #Read whole file
    #print(df)

    #data = pd.read_excel(stud_file) 
    #df = pd.DataFrame(data, columns=['Size'])  #Print a individual column
    #print(df)


    # data = pd.read_excel(stud_file) 

    # for row in data.iterrows():
    #     for cell in row:
    #         print(cell.value)
    
    # load excel with its path
    wrkbk = openpyxl.load_workbook(stud_file)
    
    sh = wrkbk.active
    
    # iterate through excel and display data
    # min row = 2 to skip titles
    for row in sh.iter_rows(min_row=2):
        for cell in row:
            print(cell.value, end=" ")
    
    '''

    


    

    


    #If the schedule creation is successfull show successful message.
    #messagebox.showinfo("Note", "Successfully formed a Schedule")

#Function for downloading scedule, maybe need this
def save_schedule():
    print('Downloading Schedule')
    messagebox.showinfo("Note", "Successfully downloaded the Schedule")

def main():
    #Setup Window
    root = tk.Tk()
    root.title('Scheduler')
    root.geometry("1920x1080")

    frame = tk.Frame(root, bg='#80c1ff', bd=5)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.85, anchor='n')
    root.configure(bg='#ADD8E6')


    #Labels
    student_list_name = customtkinter.CTkLabel(master=frame, text="", font=("Roboto Medium", -18))
    student_list_name.place(relwidth=0.40, relheight=0.1, relx=0.6, rely=0.125)

    resouce_list_name = customtkinter.CTkLabel(master=frame, text="", font=("Roboto Medium", -18))
    resouce_list_name.place(relwidth=0.40, relheight=0.1, relx=0.6, rely=0.225)

    #Buttons
    student_list = customtkinter.CTkButton(master=frame, text="Import List of Students", font=("Sitka Banner", 20, "bold"), text_color="black", command=lambda: import_excel(student_list_name,1))
    student_list.place(relx=0.4, rely=0.15,relwidth=0.15, relheight=0.05)

    resouce_list = customtkinter.CTkButton(master=frame, text="Import Class Resource",font=("Sitka Banner", 20, "bold"), text_color="black", command=lambda: import_excel(resouce_list_name,2))
    resouce_list.place(relx=0.4, rely=0.25, relwidth=0.15, relheight=0.05)
  
    create_schedule = customtkinter.CTkButton(master=frame, text="Create", font=("Sitka Banner", 20, "bold"), text_color="black", command=lambda: form_schedule(student_list_name.cget("text"),resouce_list_name.cget("text")))
    create_schedule.place(relx=0.4, rely=0.35, relwidth=0.15, relheight=0.05)

    download_schedule = customtkinter.CTkButton(master=frame, text="Download", font=("Sitka Banner", 20, "bold"), text_color="black", command=lambda: save_schedule())
    download_schedule.place(relx=0.4, rely=0.45, relwidth=0.15, relheight=0.05)

    root.mainloop()


main()