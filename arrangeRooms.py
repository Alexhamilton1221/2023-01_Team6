from Database.classrooms import Classrooms
def get_hours():
    # This is the amount of hours for coures per classroom (for either core or program, but not together)
    hours_per_day = 8
    days = 24
    return hours_per_day * days


def get_FullStack_hours():
    # This is the amount of hours for fullstack courstack
    hours_per_day = 3.5
    days = 24
    return hours_per_day * days
