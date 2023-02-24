#modules
import tkinter as tk
from tkinter import *
from tkinter import ttk
import customtkinter
import gui_functions as gu
#Global variables for 2 excel paths
stud_file=''
res_file=''


    
def main():
    #Setup Window
    root = tk.Tk()
    root.title('Scheduler')
    root.geometry("1920x1080")

    #custom colours
    mygreen = "#d2ffd2"
    myred = "#dd0202"
    myblue="#ADD8E6"
    
    #Settup Tab Control & Tabs
    tabControl = ttk.Notebook(root)
    information_tab = ttk.Frame(tabControl)
    schedule_tab = ttk.Frame(tabControl)


    #Create Style for Tab_Bar
    style = ttk.Style()
    style.theme_create( "Tab_Style", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": mygreen },
            "map":       {"background": [("selected", myred)],
                          "expand": [("selected", [4, 4, 4, 0])] } } } )

    style.theme_use("Tab_Style")
    style.configure("TNotebook", background=myblue)
    

    #Create All Tabs
    tabControl.add(information_tab, text ='Information')
    tabControl.add(schedule_tab, text ='Schedule')


###################################################################################################
    #Information Tab

    #Information Tab Frames
    frame_t1_background = tk.Frame(information_tab, bg='#80c1ff', bd=5)
    frame_t1_background.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor='n')
    
    frame_t1_displaycore = tk.Frame(information_tab, bd=5)
    frame_t1_displaycore.place(relx=0.375, rely=0.1, relwidth=0.7, relheight=0.2, anchor='n')
    
    frame_t1_displayrest = tk.Frame(information_tab, bd=5)
    frame_t1_displayrest.place(relx=0.375, rely=0.4, relwidth=0.7, relheight=0.5, anchor='n')
    
    frame_t1_totals = tk.Frame(information_tab, bd=5)
    frame_t1_totals.place(relx=0.85, rely=0.1, relwidth=0.15, relheight=0.8, anchor='n')
    
    #Information Tab Labels for Totals
    
    #Plain Text Labels
    totals = customtkinter.CTkLabel(master=frame_t1_totals, text="Totals", font=("Roboto Medium", -18))
    totals.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.001)
    
    #Labels that print Totals from inputed data using generate button

    info_label_totals=[] ;  info_label_totals_y=[0.05,0.1,0.5,0.55,0.6,0.65,0.7]
    for i in range(0,7,1):
        new_lbl = customtkinter.CTkLabel(master=frame_t1_totals, text="test", font=("Roboto Medium", -18))
        new_lbl.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=info_label_totals_y[i])  
        info_label_totals.append(new_lbl)
    
    
    #Labels for excel file names
    student_list_name = customtkinter.CTkLabel(master=frame_t1_background, text="", font=("Roboto Medium", -18))
    student_list_name.place(relwidth=0.40, relheight=0.1, relx=0.025, rely=0.89)

    resouce_list_name = customtkinter.CTkLabel(master=frame_t1_background, text="", font=("Roboto Medium", -18))
    resouce_list_name.place(relwidth=0.40, relheight=0.1, relx=0.36, rely=0.89)
    
    
    #Create Buttons 
    btn_student_list = Button(frame_t1_background,borderwidth=0,command=lambda: gu.import_excel(student_list_name,1))
    student_list_img = PhotoImage(file="Images\import_students.png") 
    btn_student_list.config(image=student_list_img)
    btn_student_list.place(relx=0.022, rely=0.92,relwidth=0.10, relheight=0.035)
    
    btn_classroom_list = Button(frame_t1_background,borderwidth=0,command=lambda: gu.import_excel(resouce_list_name,2))
    clsasroom_list_img = PhotoImage(file="Images\import_classrooms.png") 
    btn_classroom_list.config(image=clsasroom_list_img)
    btn_classroom_list.place(relx=0.35, rely=0.92,relwidth=0.11, relheight=0.035)
    
    
    btn_generate_schedule = Button(frame_t1_background,borderwidth=0,command=lambda: gu.form_schedule(student_list_name.cget("text"),resouce_list_name.cget("text")))
    generate_schedule_img = PhotoImage(file="Images\generate_schedule.png") 
    btn_generate_schedule.config(image=generate_schedule_img)
    btn_generate_schedule.place(relx=0.65, rely=0.92,relwidth=0.065, relheight=0.035)
    

    
    btn_download_schedule = Button(frame_t1_background,borderwidth=0,command=lambda: gu.save_schedule())
    download_schedule_img = PhotoImage(file="Images\download_schedule.png") 
    btn_download_schedule.config(image=download_schedule_img)
    btn_download_schedule.place(relx=0.80, rely=0.92,relwidth=0.065, relheight=0.035)
    
    
    
    #Information Tab Labels for Core Courses
    info_label_core_names={"lbl0":"Core Courses","lbl1":"Term 1","lbl2":"Term 2","lbl3":"Term 3","lbl4":"PCOM","lbl5":"BCOM"}
    info_label_core=[] ; info_label_core_x=[0.01,0.25,0.50,0.75,0.01,0.01] ;info_label_core_y=[0.025,0.025,0.025,0.025,0.25,0.475]
    info_label_rel_width=[0.2,0.10,0.10,0.10,0.20,0.20]
    for i in range(0,6,1):
        text=info_label_core_names[f"lbl{i}"]
        info_label_core_names[f"lbl{i}"] = customtkinter.CTkLabel(master=frame_t1_displaycore, text=f"{text}", font=("Roboto Medium", -18))
        info_label_core_names[f"lbl{i}"].place(relwidth=info_label_rel_width[i], relheight=0.1, relx=info_label_core_x[i], rely=info_label_core_y[i])  
        info_label_core.append(info_label_core_names[f"lbl{i}"])
   
    #Creates 23 StrVars and set values to zero for all Spinboxes
    vars = []
    for j in range(0,23,1):
        var = StringVar(root,value=0)
        vars.append(var)

    #Create Spinbox Objects for Core Courses
    core_spn=[]; core_spn_xvals=[0.28,0.53,0.78] 
    spn_names_core={"spn_0":"spn_pcom_t1","spn_1":"spn_pcom_t2","spn_2":"spn_pcom_t3","spn_3":"spn_bcom_t1","spn_4":"spn_bcom_t2","spn_5":"spn_bcom_t3"}
    for i in range(0,6,1):
        if i>=3:
            spn_names_core[f"spn_{i}"]=ttk.Spinbox(frame_t1_displaycore,from_=0,to=100,wrap=True,textvariable=vars[i])  
            spn_names_core[f"spn_{i}"].place(relwidth=0.05, relheight=0.13, relx=core_spn_xvals[i-3], rely=0.475)
            core_spn.append(spn_names_core[f"spn_{i}"])
        
        else:
            spn_names_core[f"spn_{i}"]=ttk.Spinbox(frame_t1_displaycore,from_=0,to=100,wrap=True,textvariable=vars[i])  
            spn_names_core[f"spn_{i}"].place(relwidth=0.05, relheight=0.13, relx=core_spn_xvals[i], rely=0.25)
            core_spn.append(spn_names_core[f"spn_{i}"])

    #Create Spinbox Objects for Non-Core Courses
    non_core_spn=[]; pcom_spn_xvals=[0.28,0.53,0.78] 
    spn_names_noncore={"spn_0":"spn_pm_t1","spn_1":"spn_pm_t2","spn_2":"spn_pm_t3","spn_3":"spn_ba_t1","spn_4":"spn_ba_t2","spn_5":"spn_ba_t3"
                    ,"spn_6":"spn_glm_t1","spn_7":"spn_glm_t2","spn_8":"spn_glm_t3","spn_9":"spn_fs_t1","spn_10":"spn_fs_t2","spn_11":"spn_fs_t3"
                    ,"spn_12":"spn_dxd_t1","spn_13":"spn_dxd_t2","spn_14":"spn_dxd_t3"}
    for j in range(0,15,1):
        if j>=3 and j<6:
            spn_names_noncore[f"spn_{j}"]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i])  
            spn_names_noncore[f"spn_{j}"].place(relwidth=0.05, relheight=0.05, relx=pcom_spn_xvals[j-3], rely=0.28)
            non_core_spn.append(spn_names_noncore[f"spn_{j}"])
        elif j>=6 and j<9:
            spn_names_noncore[f"spn_{j}"]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i])  
            spn_names_noncore[f"spn_{j}"].place(relwidth=0.05, relheight=0.05, relx=pcom_spn_xvals[j-6], rely=0.38)
            non_core_spn.append(spn_names_noncore[f"spn_{j}"])
        elif j>=9 and j<12:
            spn_names_noncore[f"spn_{j}"]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i])  
            spn_names_noncore[f"spn_{j}"].place(relwidth=0.05, relheight=0.05, relx=pcom_spn_xvals[j-9], rely=0.48)
            non_core_spn.append(spn_names_noncore[f"spn_{j}"])
        elif j>=12 and j<15:
            spn_names_noncore[f"spn_{j}"]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i])  
            spn_names_noncore[f"spn_{j}"].place(relwidth=0.05, relheight=0.05, relx=pcom_spn_xvals[j-12], rely=0.58)
            non_core_spn.append(spn_names_noncore[f"spn_{j}"])  
        else:
            spn_names_noncore[f"spn_{j}"]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i])  
            spn_names_noncore[f"spn_{j}"].place(relwidth=0.05, relheight=0.05, relx=pcom_spn_xvals[j], rely=0.18)
            non_core_spn.append(spn_names_noncore[f"spn_{j}"])
        i+=1
   
    #Information Tab Labels for Non Core Courses
    info_label_core_names={"lbl0":"Non Core Courses","lbl1":"Term 1","lbl2":"Term 2","lbl3":"Term 3","lbl4":"PM","lbl5":"BA","lbl6":"GLM","lbl7":"FS","lbl8":"DXD"}
    info_label_core=[] ; info_label_core_x=[0.01,0.25,0.50,0.75,0.01,0.01,0.01,0.01,0.01] ;info_label_core_y=[0.025,0.025,0.025,0.025,0.15,0.25,0.35,0.45,0.55]
    info_label_rel_width=[0.2,0.10,0.10,0.10,0.20,0.20,0.20,0.20,0.20]
    for i in range(0,9,1):
        text=info_label_core_names[f"lbl{i}"]
        info_label_core_names[f"lbl{i}"] = customtkinter.CTkLabel(master=frame_t1_displayrest, text=f"{text}", font=("Roboto Medium", -18))
        info_label_core_names[f"lbl{i}"].place(relwidth=info_label_rel_width[i], relheight=0.1, relx=info_label_core_x[i], rely=info_label_core_y[i])  
        info_label_core.append(info_label_core_names[f"lbl{i}"])
        
  
###################################################################################################
    #Schedule Tab    

    #Information Tab Frames
    frame_t2_background = tk.Frame(schedule_tab, bg='#80c1ff', bd=5)
    frame_t2_background.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor='n')

    frame_t2_schedule = tk.Frame(schedule_tab, bd=5)
    frame_t2_schedule.place(relx=0.65, rely=0.2, relwidth=0.6, relheight=0.7, anchor='n')
    
   

    #Information Canvas

    #Create Dropdown for Classrooms
    var_dispclass = StringVar(root) ; var_dispclass.set("one") 
    dispclass = OptionMenu(frame_t2_background, var_dispclass, "one", "two", "three") #Replace Default Values with Classrooms
    dispclass.place(relx=0.85, rely=0.15, relwidth=0.05, relheight=0.025, anchor='n')
    
  
    #Create Dropdown for Weeks
    weeks=["Week 1", "Week 2","Week 3","Week 4","Week 5","Week 6","Week 7","Week 8","Week 9"]
    var_display_week = StringVar(root) ; var_display_week.set(weeks[0]) 
    #display_week=OptionMenu(frame_t2_background, var_display_week, *weeks,command=lambda: gu.form_schedule_screen()) #Replace Default Values with Classrooms
    display_week=tk.OptionMenu(frame_t2_background, var_display_week, *weeks,command=lambda x: gu.form_schedule_screen(frame_t2_background)) #Replace Default Values with Classrooms

    display_week.place(relwidth=0.05, relheight=0.025, relx=0.5, rely=0.15)

    # Create labels for each day of the week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    for i, day in enumerate(days):
        tk.Label(frame_t2_schedule, text=day).grid(row=0, column=i+1)

    # Create labels for each class period
    times =["6:00 am", "6:30 am", "7:00 am", "7:30 am", "8:00 am", "8:30 am",
             "9:00 am", "9:30 am", "10:00 am", "10:30 am", "11:00 am",
             "11:30 am",
             "12:00 pm", "12:30 pm", "1:00 pm", "1:30 pm", "2:00 pm", "2:30 pm",
             "3:00 pm", "3:30 pm",
             "4:00 pm", "4:30 pm", "5:00 pm", "5:30 pm", "6:00 pm", "6:30 pm",
             "7:00 pm"]
    for i, time in enumerate(times):
        tk.Label(frame_t2_schedule, text=time).grid(row=i+1, column=0)

    # Create entry boxes for each class
    entries = {}
    for i, time in enumerate(times):
        for j, day in enumerate(days):
            #In here check for timeslots that classroom is using
            entry = tk.Entry(frame_t2_schedule,bg='red')
            entry.grid(row=i+1, column=j+1, sticky="nsew")
            entry.config(state=DISABLED) #Make it so that nobody can type into class
            entries[(i, j)] = entry
    

    #Screen Setup
    tabControl.pack(expand = 1, fill ="both")
    root.mainloop()  

main()