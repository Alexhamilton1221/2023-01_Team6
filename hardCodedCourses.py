from Database.cohort import Cohort
from Database.storedcourse import StoredCourse
from Database.program import Program
def temp_create_courses():
    # This is a temp file meant for storing the information from the program before we have an excel system working
    PCOM = Program("PCOM")
    # PCOM TERM 1
    PCOM.add_course(StoredCourse("PCOM 0101", 35, 1, []))
    PCOM.add_course(StoredCourse("PCOM 0105", 35, 1, []))
    PCOM.add_course(StoredCourse("PCOM 0107", 18, 1, [], "Lab"))
    PCOM.add_course(StoredCourse("CMSK 0233", 7, 1, [], "Lab"))
    PCOM.add_course(StoredCourse("CMSK 0235", 6, 1, [], "Lab"))
    # PCOM TERM 2
    PCOM.add_course(StoredCourse("PCOM 0102", 35, 2, []))
    PCOM.add_course(StoredCourse("PCOM 0201", 35, 2, []))
    PCOM.add_course(StoredCourse("PCOM 0108", 18, 2, [], "Lab"))
    # PCOM TERM 3
    PCOM.add_course(StoredCourse("PCOM 0202", 33, 3, []))
    PCOM.add_course(StoredCourse("PCOM 0103", 35, 3, []))
    PCOM.add_course(StoredCourse("PCOM 0109 Class", 6, 3, [], "Class", "H=2"))
    PCOM.add_course(StoredCourse("PCOM 0109 Lab", 8, 3, [], "Lab", "H=2"))

    BCOM = Program("BCOM")
    # BCOM TERM 1
    BCOM.add_course(StoredCourse("PCOM 0203", 15, 1, []))
    BCOM.add_course(StoredCourse("SUPR 0751", 7, 1, [], "Class", "H=2"))
    BCOM.add_course(StoredCourse("PCOM 0204", 35, 1, []))
    BCOM.add_course(StoredCourse("CMSK 0237", 12, 1, [], "Online"))
    BCOM.add_course(StoredCourse("SUPR 0837", 7, 1, [], "Class", "H=2"))
    BCOM.add_course(StoredCourse("SUPR 0841", 7, 1, [], "Class", "H=2"))

    # BCOM TERM 2
    BCOM.add_course(StoredCourse("SUPR 0821", 7, 2, [], "Class", "H=2"))
    BCOM.add_course(StoredCourse("SUPR 0822", 7, 2, [], "Class", "H=2"))
    BCOM.add_course(StoredCourse("SUPR 0718", 7, 2, [], "Class", "H=2"))
    BCOM.add_course(StoredCourse("SUPR 0836", 7, 2, [], "Online"))
    BCOM.add_course(StoredCourse("AVDM 0199", 3, 2, [], "Class", "H=2"))
    BCOM.add_course(StoredCourse("PCOM 0106", 35, 2, [], "Class", "H=2"))

    # BCOM TERM 3
    BCOM.add_course(StoredCourse("PCOM 0205", 30, 3, [], "Class", "H=3"))
    BCOM.add_course(StoredCourse("PCOM TBD", 21, 3, []))
    BCOM.add_course(StoredCourse("PCOM 0207", 6, 3, [], "Class", "H=2"))
    BCOM.add_course(StoredCourse("SUPR 0863", 7, 3, [], "Class", "H=2"))
    BCOM.add_course(StoredCourse("AVDM 0206", 6, 3, [], "Class", "H=3"))
    BCOM.add_course(StoredCourse("AVDM 0260", 6, 3, [], "Online"))

    # Project Management
    PM = Program("PM")
    # Term 1
    PM.add_course(StoredCourse("PRDV 0201", 21, 1, []))
    PM.add_course(StoredCourse("PRDV 0202", 14, 1, []))
    PM.add_course(StoredCourse("PRDV 0203", 21, 1, []))
    # Term 2
    PM.add_course(StoredCourse("PRDV 0204", 14, 2, []))
    PM.add_course(StoredCourse("PRDV 0205", 21, 2, []))
    PM.add_course(StoredCourse("PCOM 0130", 21, 2, [], "Class", "T=half"))
    PM.add_course(StoredCourse("PRDV 0206", 14, 2, []))
    # Term 3
    PM.add_course(StoredCourse("PRDV 0207", 14, 3, []))
    PM.add_course(StoredCourse("PCOM 0131", 39, 3, [], "Class", "H=3"))

    # Business Analysis
    BA = Program("BA")
    # Term 1
    BA.add_course(StoredCourse("PRDV 0640", 21, 1, []))
    BA.add_course(StoredCourse("PRDV 0652", 14, 1, []))
    BA.add_course(StoredCourse("PRDV 0653", 21, 1, []))
    BA.add_course(StoredCourse("PRDV 0642", 14, 1, []))
    # Term 2
    BA.add_course(StoredCourse("PRDV 0644", 21, 2, []))
    BA.add_course(StoredCourse("PRDV 0648", 14, 2, []))
    BA.add_course(StoredCourse("PCOM 0140", 35, 2, [], "Class", "T=half"))
    # Term 3
    BA.add_course(StoredCourse("PRDV 0646", 14, 3, []))
    BA.add_course(StoredCourse("PCOM 0141", 39, 3, [], "Class", "H=3"))

    # Business Analysis
    GLM = Program("GL")
    # Term 1
    GLM.add_course(StoredCourse("SCMT 0501", 21, 1, []))
    GLM.add_course(StoredCourse("SCMT 0502", 21, 1, []))
    GLM.add_course(StoredCourse("PRDV 0304", 15, 1, []))
    # Term 2
    GLM.add_course(StoredCourse("SCMT 0503", 15, 2, []))
    GLM.add_course(StoredCourse("SCMT 0504", 21, 2, []))
    # Term 3
    GLM.add_course(StoredCourse("SCMT 0505", 21, 3, []))
    GLM.add_course(StoredCourse("PCOM 0151", 39, 3, [], "Class", "H=3"))

    # Full Stack Web
    FS = Program("FS")
    # Term 1
    FS.add_course(StoredCourse("CMSK 0150", 16, 1, [], "Lab", "H=2"))
    CMSK151 = StoredCourse("CMSK 0151", 16, 1, [], "Lab", "H=2")
    FS.add_course(CMSK151)
    CMSK152 = StoredCourse("CMSK 0152", 16, 1, [CMSK151], "Lab", "H=2")
    FS.add_course(CMSK152)
    CMSK157 = StoredCourse("CMSK 0157", 16, 1, [], "Lab", "H=2|COREC=CMSK 0154")
    FS.add_course(CMSK157)
    CMSK154 = StoredCourse("CMSK 0154", 16, 1, [], "Lab", "H=2|COREC=CMSK 0157")
    FS.add_course(CMSK154)

    # Term 2

    CMSK153 = StoredCourse("CMSK 0153", 18, 2, [], "Lab", "H=2")
    FS.add_course(CMSK153)
    CMSK200 = StoredCourse("CMSK 0200", 16, 2, [], "Lab", "H=2")
    FS.add_course(CMSK200)
    CMSK201 = StoredCourse("CMSK 0201", 18, 2, [CMSK200], "Lab", "H=2")
    FS.add_course(CMSK201)
    CMSK202 = StoredCourse("CMSK 0202", 16, 2, [CMSK201], "Lab", "H=2|COREC=CMSK 0203")
    FS.add_course(CMSK202)
    CMSK203 = StoredCourse("CMSK 0203", 18, 2, [], "Lab", "H=2|COREC=CMSK 0202")
    FS.add_course(CMSK203)

    # Term 3
    FS.add_course(StoredCourse("PCOM 0160", 50, 3, [], "Lab", "H=3"))

    # Digital Experience Design
    DXD = Program("DXD")
    # Term 1
    DXD.add_course(StoredCourse("ADVM 0165", 18, 1, [], "Lab"))
    DXDI101 = StoredCourse("DXD 0101", 24, 1, [], "Lab")
    DXD.add_course(DXDI101)
    DXDI102 = StoredCourse("DXD 0102", 24, 1, [DXDI101], "Lab")
    DXD.add_course(DXDI102)

    # Term 2
    DXD.add_course(StoredCourse("ADVM 0170", 18, 2, [], "Lab"))
    DXD.add_course(StoredCourse("ADVM 0138", 18, 2, [], "Lab"))
    DXDI103 = StoredCourse("DXD 0103", 24, 2, [], "Lab")
    DXD.add_course(DXDI103)
    DXDI104 = StoredCourse("DXD 0104", 24, 2, [DXDI103], "Lab")
    DXD.add_course(DXDI104)
    # Term 3
    DXD.add_course(StoredCourse("ADVM 0238", 18, 3, [], "Lab"))
    DXD.add_course(StoredCourse("ADVM 0270", 18, 3, [], "Lab"))
    DXD.add_course(StoredCourse("DXDI 9901", 45, 3, [], "Lab"))

    # Bookkeeping Certificate
    BC = Program("BK")
    # Term 1
    BC.add_course(StoredCourse("ACCT 0201", 18, 1, []))
    BC.add_course(StoredCourse("ACCT 0202", 12, 1, []))
    BC.add_course(StoredCourse("ACCT 0203", 12, 1, []))
    # Term 2
    BC.add_course(StoredCourse("ACCT 0206", 12, 2, []))
    BC.add_course(StoredCourse("ACCT 0210", 28, 2, [], "Lab"))
    BC.add_course(StoredCourse("ACCT 0211", 28, 2, [], "Lab"))
    # Term 3
    BC.add_course(StoredCourse("SCMT 0505", 21, 3, []))
    BC.add_course(StoredCourse("PCOM 0151", 33, 3, [], "Class", "H=3"))

    return [PCOM, BCOM, PM, BA, GLM, FS, DXD, BC]


temp_create_courses()

