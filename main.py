#modules
import tkinter as tk
from tkinter import *
from tkinter import ttk
import customtkinter
import gui_functions as gu
from tkinter import font
import tkinter.font as tkFont
import hardCodedClassrooms as cl
from Database.programs import Programs
from Database.cohorts import NearLimit
from Database.cohorts import OverLimit
from Database.programs import Programs
from hardCodedCourses import temp_create_courses
from Database.classrooms import Classrooms
from Database.classroom import Classroom
from hardCodedClassrooms import temp_Classroom_add
from Database.cohorts import Cohorts
from Database.cohort import Cohort


#Global variables for 2 excel paths
stud_file=''
res_file=''
classroom_list = cl.temp_Classroom_add()

# TEMP - runs test to create schedule based of dummy data
def test_given_cohorts_make_schedules_for_all():
    global classroom_list
    programs = Programs(temp_create_courses())
    classrooms = Classrooms(classroom_list)
    students = [["PCOM 1", 60], ["PCOM 3", 40], ["BA 1", 46], ["BA 3", 30], ["DXD 1", 60],
                ["BK 1", 36]]

    cohorts = Cohorts()
    cohorts.create_cohorts(classrooms, programs, students, 2)
    cohorts.create_schedules(2)
    gu.print_schedule(classrooms)

    for room in classrooms.get_rooms():
        room.check_for_conflict()

    return(classrooms)

test_given_cohorts_make_schedules_for_all()

# Runs when either week or class is updated on schedule tab
# Clears the entries and iterates through global list of classroom objects
# If the room matches the one selected, iterate through all courses assigned to that room
# For each lecture, if it is within the week selected create a schedule block for it
def update_schedule(*args):
    # Refrences class selected, all classroom objects, the schedule grid, and the seleced week
    global classroom_label, classroom_list, entries, var_display_week
    # Clear schedule for new blocks
    gu.clear_schedule(entries)
    # New selection from dropdown, can be a week or a classroom
    data = args[0]

    # Get current week from global dropdown variable
    week = int(var_display_week.get()[-1])
    
    # If the classroom dropdown has changed, not the week
    if 'Week' not in data:
        #Change label to reflect new choice
        classroom_label.configure(text=str(data))

    #For each room in global list of classroom objects
    for room in classroom_list:
        #If room matches selected
        if room.name == classroom_label.cget('text'):
            for cohort in room.cohorts:
                for course in cohort.courses:
                    # For each lecture for each course assigned to this room
                    for lecture in course.lectures:
                        # If lecture day within range of selected week
                        if (lecture.day-1) - ((week-1)*4) in range(4):
                            # Make sure course delivery and room match, create blocks
                            if course.delivery == 'Class' and room.is_lab == False:
                                gu.create_schedule_block(entries, lecture, course.name, cohort)
                            elif course.delivery == 'Lab' and room.is_lab == True:
                                gu.create_schedule_block(entries, lecture, course.name, cohort)
def main():
    #Setup Window
    root = tk.Tk()
    root.title('Scheduler')
    root.geometry("1280x720")

    #custom colours
    mygreen = "#d2ffd2"
    myred = "#8B2332"
    mydarkred="#781C29"
    myblue="#ADD8E6"
    mytext="#FFFFFF"
    myframebg = "#252526"
    mygrey="#3e3e42"
    #Settup Tab Control & Tabs
    tabControl = ttk.Notebook(root)
    information_tab = ttk.Frame(tabControl)
    schedule_tab = ttk.Frame(tabControl)

    global classroom_list
    


    #Create Style for Tab_Bar
    style = ttk.Style()
    style.theme_create( "Tab_Style", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"foreground": (mytext), #TODO - Change tab text color
            "padding": [5, 1], "background": mydarkred },
            "map":       {"background": [("selected", '#3e3e42')],
                          "expand": [("selected", [4, 4, 4, 0])] } } } )

    style.theme_use("Tab_Style")
    style.configure("TNotebook", background=myframebg)
    
    #Create Fonts
    roboto_14=customtkinter.CTkFont(family='Roboto Medium', size=12)
    roboto_18=customtkinter.CTkFont(family='Roboto Medium', size=-18)
    helv36 = tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD)
    #helv40 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)


    #Create All Tabs
    tabControl.add(information_tab, text ='Information')
    tabControl.add(schedule_tab, text ='Schedule')


###################################################################################################
    #Information Tab

    #Information Tab Frames
    frame_t1_background = tk.Frame(information_tab, bg=mygrey, bd=5)
    frame_t1_background.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor='n')
    
    frame_t1_displaycore = tk.Frame(information_tab, bd=5, bg=myframebg)
    frame_t1_displaycore.place(relx=0.375, rely=0.1, relwidth=0.7, relheight=0.2, anchor='n')
    
    frame_t1_displayrest = tk.Frame(information_tab, bd=5, bg=myframebg)
    frame_t1_displayrest.place(relx=0.375, rely=0.4, relwidth=0.7, relheight=0.5, anchor='n')
    
    frame_t1_totals = tk.Frame(information_tab, bd=5, bg=myframebg)
    frame_t1_totals.place(relx=0.85, rely=0.1, relwidth=0.15, relheight=0.8, anchor='n')
    
    #Information Tab Labels for Totals
    
    #Plain Text Labels
    totals = customtkinter.CTkLabel(master=frame_t1_totals, text="Totals", font=roboto_18,text_color=mytext, )
    totals.place(relwidth=0.3, relheight=0.05, relx=0.365, rely=0.001)
    
    #Labels that print Totals from inputed data using generate button

    info_label_totals=[] ;  info_label_totals_y=[0.065,0.125,0.45,0.55,0.65,0.75,0.85,0.95]
    for i in range(0,8,1):
        new_lbl = customtkinter.CTkLabel(master=frame_t1_totals, text=0, font=roboto_18,text_color=mytext)
        new_lbl.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=info_label_totals_y[i])  
        info_label_totals.append(new_lbl)
    
    
    #Labels for excel file names
    student_list_name = customtkinter.CTkLabel(master=frame_t1_background, text="", font=roboto_14,text_color=mytext)
    student_list_name.place(relwidth=0.40, relheight=0.1, relx=0.05, rely=0.89)

    resouce_list_name = customtkinter.CTkLabel(master=frame_t1_background, text="", font=roboto_14, text_color=mytext)
    resouce_list_name.place(relwidth=0.40, relheight=0.1, relx=0.41, rely=0.89)
    
    



    #Information Tab Labels for Core Courses
    info_label_core_names={"lbl0":"Core Courses","lbl1":"Term 1","lbl2":"Term 2","lbl3":"Term 3","lbl4":"PCOM","lbl5":"BCOM"}
    info_label_core=[] ; info_label_core_x=[0.01,0.21,0.46,0.71,0.01,0.01] ;info_label_core_y=[0.025,0.025,0.025,0.025,0.25,0.475]
    info_label_rel_width=[0.2,0.20,0.20,0.20,0.20,0.20]
    for i in range(0,6,1):
        text=info_label_core_names[f"lbl{i}"]
        info_label_core_names[f"lbl{i}"] = customtkinter.CTkLabel(master=frame_t1_displaycore, text=f"{text}", font=roboto_18, text_color=mytext)
        info_label_core_names[f"lbl{i}"].place(relwidth=info_label_rel_width[i], relheight=0.15, relx=info_label_core_x[i], rely=info_label_core_y[i])  
        info_label_core.append(info_label_core_names[f"lbl{i}"])
   
    #Creates 23 StrVars and set values to zero for all Spinboxes
    vars = []
    for j in range(0,26,1):
        var = StringVar(root,value=0)
        vars.append(var)

    #Create Spinbox Objects for Core Courses
    core_spn_xvals=[0.28,0.53,0.78] 
    spn_core={"spn_pcom_t1": "spn_0","spn_pcom_t2" :"spn_1","spn_pcom_t3":"spn_2","spn_bcom_t1": "spn_3","spn_bcom_t2":"spn_4","spn_bcom_t3":"spn_5"}
    spn_names = [];    spn_core_obj=[]

    for i, spn in enumerate(spn_core):
        if i>=3:
            spn_core[spn] =ttk.Spinbox(frame_t1_displaycore,from_=0,to=100,wrap=True,textvariable=vars[i],command=lambda : gu.update_totals(spn_core,info_label_totals,2,spn_core_obj))  
            spn_core[spn].place(relwidth=0.05, relheight=0.21, relx=core_spn_xvals[i-3], rely=0.5)
            spn_core[spn].bind("<Return>", lambda event: gu.update_totals(spn_core,info_label_totals,2,spn_core_obj))
        
        else:
            spn_core[spn]=ttk.Spinbox(frame_t1_displaycore,from_=0,to=100,wrap=True,textvariable=vars[i],command=lambda : gu.update_totals(spn_core,info_label_totals,1,spn_core_obj))  
            spn_core[spn].place(relwidth=0.05, relheight=0.21, relx=core_spn_xvals[i], rely=0.25)
            spn_core[spn].bind("<Return>", lambda event: gu.update_totals(spn_core,info_label_totals,1,spn_core_obj))

        spn_names.append(spn)
        spn_core_obj.append(spn_core[spn])

    #Create Spinbox Objects for Non-Core Courses
    pcom_spn_xvals=[0.28,0.53,0.78] 
    spn_noncore={'spn_pm_t1': 'spn_0', 'spn_pm_t2': 'spn_1', 'spn_pm_t3': 'spn_2', 'spn_ba_t1': 'spn_3', 'spn_ba_t2': 'spn_4', 
                       'spn_ba_t3': 'spn_5', 'spn_gl_t1': 'spn_6', 'spn_gl_t2': 'spn_7', 'spn_gl_t3': 'spn_8', 'spn_fs_t1': 'spn_9', 
                       'spn_fs_t2': 'spn_10', 'spn_fs_t3': 'spn_11', 'spn_dxd_t1': 'spn_12', 'spn_dxd_t2': 'spn_13', 'spn_dxd_t3': 'spn_14',
                       'spn_bk_t1': 'spn_15', 'spn_bk_t2': 'spn_16', 'spn_bk_t3': 'spn_17'}
    spn_noncore_obj=[]
    i+=1
    for j, spn in enumerate(spn_noncore):
        if j>=3 and j<6:
            spn_noncore[spn]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i],command=lambda : gu.update_totals(spn_noncore,info_label_totals,4,spn_noncore_obj))  
            spn_noncore[spn].place(relwidth=0.05, relheight=0.08, relx=pcom_spn_xvals[j-3], rely=0.30)
            spn_noncore[spn].bind("<Return>", lambda event: gu.update_totals(spn_noncore,info_label_totals,4,spn_noncore_obj))

        elif j>=6 and j<9:
            spn_noncore[spn]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i],command=lambda : gu.update_totals(spn_noncore,info_label_totals,5,spn_noncore_obj))  
            spn_noncore[spn].place(relwidth=0.05, relheight=0.08, relx=pcom_spn_xvals[j-6], rely=0.45)
            spn_noncore[spn].bind("<Return>", lambda event: gu.update_totals(spn_noncore,info_label_totals,5,spn_noncore_obj))

        elif j>=9 and j<12:
            spn_noncore[spn]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i],command=lambda : gu.update_totals(spn_noncore,info_label_totals,6,spn_noncore_obj))  
            spn_noncore[spn].place(relwidth=0.05, relheight=0.08, relx=pcom_spn_xvals[j-9], rely=0.60)
            spn_noncore[spn].bind("<Return>", lambda event: gu.update_totals(spn_noncore,info_label_totals,6,spn_noncore_obj))

        elif j>=12 and j<15:
            spn_noncore[spn]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i],command=lambda : gu.update_totals(spn_noncore,info_label_totals,7,spn_noncore_obj))  
            spn_noncore[spn].place(relwidth=0.05, relheight=0.08, relx=pcom_spn_xvals[j-12], rely=0.75)
            spn_noncore[spn].bind("<Return>", lambda event: gu.update_totals(spn_noncore,info_label_totals,7,spn_noncore_obj))

        elif j>=15 and j<18:
            spn_noncore[spn]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i],command=lambda : gu.update_totals(spn_noncore,info_label_totals,8,spn_noncore_obj))  
            spn_noncore[spn].place(relwidth=0.05, relheight=0.08, relx=pcom_spn_xvals[j-15], rely=0.90)
            spn_noncore[spn].bind("<Return>", lambda event: gu.update_totals(spn_noncore,info_label_totals,8,spn_noncore_obj))

        else:
            spn_noncore[spn]=ttk.Spinbox(frame_t1_displayrest,from_=0,to=100,wrap=True,textvariable=vars[i],command=lambda : gu.update_totals(spn_noncore,info_label_totals,3,spn_noncore_obj))  
            spn_noncore[spn].place(relwidth=0.05, relheight=0.08, relx=pcom_spn_xvals[j], rely=0.15)
            spn_noncore[spn].bind("<Return>", lambda event: gu.update_totals(spn_noncore,info_label_totals,3,spn_noncore_obj))

        
        spn_names.append(spn)
        spn_noncore_obj.append(spn_noncore[spn])

        i+=1
   
    # Place Term Header for Non Core Courses
    info_label_noncore=[] ; info_label_noncore_x=[0.21,0.46,0.71]
    for i in range(3):
        term_label = customtkinter.CTkLabel(master=frame_t1_displayrest, text=f"Term {i+1}", font=roboto_18, text_color=mytext)
        term_label.place(relwidth=0.2, relheight=0.1, relx=info_label_noncore_x[i], rely=0.025)
        info_label_noncore.append(term_label)

    noncore_label_text = ["PM", "BA", "GLM", "FS", "DXD", "BK"]
    for i, label_text in enumerate(noncore_label_text):
        course_label = customtkinter.CTkLabel(master=frame_t1_displayrest, text=label_text, font=roboto_18, text_color=mytext)   
        course_label.place(relwidth=0.2, relheight=0.1, relx=0.01, rely= (0.15+(0.15*(i))))
       
        '''
    #Information Tab Labels for Non Core Courses
    info_label_core_names={":"PM","lbl5":"BA","lbl6":"GLM","lbl7":"FS","lbl8":"DXD"}
    info_label_core=[] ; info_label_core_x=[0.01,0.25,0.50,0.75,0.01,0.01,0.01,0.01,0.01] ;info_label_core_y=[0.025,0.025,0.025,0.025,0.15,0.25,0.35,0.45,0.55]
    info_label_rel_width=[0.2,0.10,0.10,0.10,0.20,0.20,0.20,0.20,0.20]
    for i in range(0,9,1):
        text=info_label_core_names[f"lbl{i}"]
        info_label_core_names[f"lbl{i}"] = customtkinter.CTkLabel(master=frame_t1_displayrest, text=f"{text}", font=roboto_18, text_color=mytext)
        info_label_core_names[f"lbl{i}"].place(relwidth=info_label_rel_width[i], relheight=0.1, relx=info_label_core_x[i], rely=info_label_core_y[i])  
        info_label_core.append(info_label_core_names[f"lbl{i}"])
        
'''
         
    #Create Buttons 
    btn_student_list = Button(frame_t1_background,borderwidth=0, width=350, height=52, text= "Import Registration",bg=myred, fg=mytext, 
                              command=lambda: 
    (gu.import_excel(student_list_name,1, [spn_names, vars]),gu.update_all_totals(spn_core,spn_noncore,info_label_totals,spn_core_obj+spn_noncore_obj)))
    
    
    
    
    #student_list_img = PhotoImage(file="Images\import_students.png") 
    #btn_student_list.config(image=student_list_img)
    btn_student_list.place(relx=0.022, rely=0.92,relwidth=0.10, relheight=0.035)
    
    btn_classroom_list = Button(frame_t1_background,borderwidth=0, width=350, height=52, text="Import Classrooms",bg=myred,fg=mytext,
                                command=lambda: gu.import_excel(resouce_list_name,2))
    #clsasroom_list_img = PhotoImage(file="Images\import_classrooms.png") 
    #btn_classroom_list.config(image=clsasroom_list_img)
    btn_classroom_list.place(relx=0.375, rely=0.92,relwidth=0.11, relheight=0.035)
    
    
    btn_generate_schedule = Button(frame_t1_background,borderwidth=0,width=350, height=52, text="Generate",bg=myred,fg=mytext,
                                   command=lambda: gu.form_schedule(student_list_name.cget("text"),resouce_list_name.cget("text")))
    #generate_schedule_img = PhotoImage(file="Images\generate_schedule.png") 
    #btn_generate_schedule.config(image=generate_schedule_img)
    btn_generate_schedule.place(relx=0.75, rely=0.92,relwidth=0.065, relheight=0.035)
    

    
    btn_download_schedule = Button(frame_t1_background,borderwidth=0,width=350, height=52, text="Download",bg=myred,fg=mytext,
                                   command=lambda: gu.save_schedule())
    #download_schedule_img = PhotoImage(file="Images\download_schedule.png") 
    #btn_download_schedule.config(image=download_schedule_img)
    btn_download_schedule.place(relx=0.90, rely=0.92,relwidth=0.065, relheight=0.035)
    
    
    #Create Dropdown for Terms
    #Using temporary values, need to calc date using datetime probably & predict future terms
    # t1=gu.get_season()

    
    
    weeks=["Fall","Winter","Spring/Summer"]
    var_chosenterm = StringVar(root) ; var_chosenterm.set("Choose a Term") 
    display_week=OptionMenu(frame_t1_background, var_chosenterm, *weeks,command=lambda x: gu.term_changed(var_chosenterm,info_label_core,info_label_noncore)) #Replace Default Values with Classrooms
    display_week.place(relwidth=0.12, relheight=0.04, relx=0.02, rely=0.03)
    display_week.config(font=helv36,bg="#252526",highlightthickness=0, foreground=mytext)
    # display_week.bind("<Leave>", gu.on_leave)
    # display_week.bind("<Enter>", gu.on_enter)

  
###################################################################################################
    #Schedule Tab    

    #Schedule Tab Frames
    frame_t2_background = tk.Frame(schedule_tab, bg=myframebg, bd=5)
    frame_t2_background.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor='n')

    frame_t2_schedule = tk.Frame(schedule_tab, bd=5)
    frame_t2_schedule.place(relx=0.5, rely=0.1, relwidth=0.85, relheight=0.85, anchor='n')
    
   
    #Create Dropdown for Classrooms
    #Using temp classrooms for now, find way to get them
    class_names = []
    for room in classroom_list:
        class_names.append(room.name)
    
    var_dispclass = StringVar(root)
    var_dispclass.set(class_names[0]) 
    #var_dispclass.trace_variable('w', update_schedule)

    
    dispclass = OptionMenu(frame_t2_background, var_dispclass, *class_names, command=update_schedule) #Replace Default Values with Classrooms
    dispclass.place(relx=0.85, rely=0.03, relwidth=0.12, relheight=0.05, anchor='n')
    dispclass.config(font=helv36,bg="#252526",highlightthickness=0, foreground=mytext)

    global classroom_label
    classroom_label = customtkinter.CTkLabel(master=frame_t2_background, text=var_dispclass.get(), font=roboto_18, text_color=mytext)
    classroom_label.place(relwidth=0.2, relheight=0.1, relx=0.4, rely= 0.02)
  
    gu.form_schedule_screen(frame_t2_background)
    
    #Create Dropdown for Weeks
    #Using temporary 9 week schedule
    weeks=["Week 1", "Week 2","Week 3","Week 4","Week 5","Week 6","Week 7","Week 8","Week 9"]
    global var_display_week
    var_display_week = StringVar(root) ; var_display_week.set(weeks[0]) 
    display_week=OptionMenu(frame_t2_background, var_display_week, *weeks,command=update_schedule ) #Replace Default Values with Classrooms
    display_week.place(relwidth=0.08, relheight=0.05, relx=0.2, rely=0.03)
    display_week.config(font=helv36,bg="#252526",highlightthickness=0, foreground=mytext)


    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    for i, day in enumerate(days):
        tk.Label(frame_t2_schedule, text=day, font=roboto_18).grid(row=0, column=i+1)

    # Create labels for each class period
    times =["8:00 am", "8:30 am","9:00 am", "9:30 am", "10:00 am", "10:30 am", "11:00 am",
             "11:30 am", "12:00 pm", "12:30 pm", "1:00 pm", "1:30 pm", "2:00 pm", "2:30 pm",
             "3:00 pm", "3:30 pm", "4:00 pm", "4:30 pm", "5:00 pm"]
    for i, time in enumerate(times):
        tk.Label(frame_t2_schedule, text=time, font=roboto_18).grid(row=i+1, column=0)

    # Create entry boxes for each class
    # To set colour use disabledbackground='yellow'
    global entries
    entries = {}
    for j, day in enumerate(days):
        for i, time in enumerate(times):
            

            #In here check for timeslots that classroom is using
            entry = tk.Entry(frame_t2_schedule, width=25,font=(roboto_18), justify='center', fg='black', disabledforeground='#000000')
            entry.grid(row=i+1, column=j+1, sticky="nsew")
            entry.config(state=DISABLED) #Make it so that nobody can type into class
            entries[(j, i)] = entry

            #TODO - Possible use frames to represent courses on top of planner

    
    #Screen Setup
    tabControl.pack(expand = 1, fill ="both")
    root.mainloop()  

main()

   