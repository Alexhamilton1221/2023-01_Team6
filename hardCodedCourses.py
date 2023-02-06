from Database.cohort import Cohort
from Database.storedcourse import StoredCourse
from Database.program import Program
def temp_create_courses():
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
    PCOM.add_course(StoredCourse("PCOM 0109 Class Portion", 6, 3, []))
    PCOM.add_course(StoredCourse("PCOM 0109 Lab Portion", 8, 3, [], "Lab"))

