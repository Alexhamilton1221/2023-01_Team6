import os
import tkinter as tk
import customtkinter
from tkinter import ttk, filedialog
from tkinter import messagebox
def import_excel(file_name):
   try:
       file = filedialog.askopenfile(mode='r', filetypes=[('CSV files', '*.xlsx')])
       f_name = os.path.basename(file.name)

       if file:
           file_name.configure(text=f_name)
   except:
        messagebox.showwarning("Warning", "Failed to upload file.")

def form_schedule():
    print('Creating Schedule')

    #If the schedule creation is successfull show successful message
    messagebox.showinfo("Note", "Successfully formed a Schedule")

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
    student_list_name = customtkinter.CTkLabel(master=frame, text="Placeholder Text", font=("Roboto Medium", -18))
    student_list_name.place(relwidth=0.40, relheight=0.4, relx=0.6, rely=-0.02)

    resouce_list_name = customtkinter.CTkLabel(master=frame, text="Placeholder Text", font=("Roboto Medium", -18))
    resouce_list_name.place(relwidth=0.40, relheight=0.4, relx=0.6, rely=0.2)

    #Buttons
    student_list = customtkinter.CTkButton(master=frame, text="Import List of Students", font=("Sitka Banner", 20, "bold"), text_color="black", command=lambda: import_excel(student_list_name))
    student_list.place(relx=0.4, rely=0.15,relwidth=0.15, relheight=0.05)

    resouce_list = customtkinter.CTkButton(master=frame, text="Import Class Resource",font=("Sitka Banner", 20, "bold"), text_color="black", command=lambda: import_excel(resouce_list_name))
    resouce_list.place(relx=0.4, rely=0.25, relwidth=0.15, relheight=0.05)

    create_schedule = customtkinter.CTkButton(master=frame, text="Create", font=("Sitka Banner", 20, "bold"), text_color="black", command=lambda: form_schedule())
    create_schedule.place(relx=0.4, rely=0.35, relwidth=0.15, relheight=0.05)

    download_schedule = customtkinter.CTkButton(master=frame, text="Download", font=("Sitka Banner", 20, "bold"), text_color="black", command=lambda: save_schedule())
    download_schedule.place(relx=0.4, rely=0.45, relwidth=0.15, relheight=0.05)

    root.mainloop()


main()