from Database.cohort import Cohort
from Database.storedcourse import StoredCourse
from Database.program import Program
def temp_create_courses():
    # Mabey I could hardcode then export to excel
    PCOM = Program("PCOM")
    # PCOM TERM 1
    PCOM.add_course(StoredCourse("PCOM 0101", 35, 1, []))
    PCOM.add_course(StoredCourse("PCOM 0105", 35, 1, []))
    PCOM.add_course(StoredCourse("PCOM 0107", 18, 1, [], "Lab"))
    PCOM.add_course(StoredCourse("PCOM 0107", 7, 1, [], "Lab"))
    PCOM.add_course(StoredCourse("PCOM 0107", 6, 1, [], "Lab"))
    # PCOM TERM 2
    PCOM.add_course(StoredCourse("PCOM 0102", 35, 2, []))
    PCOM.add_course(StoredCourse("PCOM 0201", 35, 2, []))
    PCOM.add_course(StoredCourse("PCOM 0108", 18, 2, [], "Lab"))
    # PCOM TERM 3
    PCOM.add_course(StoredCourse("PCOM 0202", 33, 3, []))
    PCOM.add_course(StoredCourse("PCOM 0103", 35, 3, []))
    PCOM.add_course(StoredCourse("PCOM 0109 Class Portion", 6, 3, [], "Class", "H=2h"))
    PCOM.add_course(StoredCourse("PCOM 0109 Lab Portion", 8, 3, [], "Lab"))

    BCOM = Program("PCOM")
    # PCOM TERM 1
    BCOM.add_course(StoredCourse("PCOM 0203", 15, 1, []))
    BCOM.add_course(StoredCourse("SUPR 0751", 7, 1, [], "Class", "H=2h"))
    BCOM.add_course(StoredCourse("PCOM 0204", 35, 1, []))
    BCOM.add_course(StoredCourse("CMSK 0237", 12, 1, [], "Online"))
    BCOM.add_course(StoredCourse("SUPR 0837", 7, 1, [], "Class", "H=2h"))
    BCOM.add_course(StoredCourse("SUPR 0841", 7, 1, [], "Class", "H=2h"))

    # PCOM TERM 2
    BCOM.add_course(StoredCourse("SUPR 0821", 7, 2, [], "Class", "H=2h"))
    BCOM.add_course(StoredCourse("SUPR 0822", 7, 2, [], "Class", "H=2h"))
    BCOM.add_course(StoredCourse("SUPR 0718", 7, 2, [], "Class", "H=2h"))
    BCOM.add_course(StoredCourse("SUPR 0836", 7, 2, [], "Online"))
    BCOM.add_course(StoredCourse("AVDM 0199", 3, 2, [], "Class", "H=2h"))
    BCOM.add_course(StoredCourse("PCOM 0106", 35, 2, [], "Class", "H=2h"))

    # PCOM TERM 3
    BCOM.add_course(StoredCourse("PCOM 0205", 30, 3, [], "Class", "H=3h"))
    BCOM.add_course(StoredCourse("PCOM TBD", 21, 3, []))
    BCOM.add_course(StoredCourse("PCOM 0207", 6, 3, [], "Class", "H=2h"))
    BCOM.add_course(StoredCourse("SUPR 0863", 7, 3, [], "Class", "H=2h"))
    BCOM.add_course(StoredCourse("AVDM 0206", 6, 3, [], "Class", "H=3h"))
    BCOM.add_course(StoredCourse("AVDM 0260", 6, 3, [], "Online"))


    print(PCOM.get_term_hours(1))

temp_create_courses()

