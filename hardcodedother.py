

def get_term_length(cur_semester):
    # Gets the length of a term (INCLUDING HOLIDAYS)
    # Shifted by 2 to accomodate starting on a wendsday
    if cur_semester == 1:
        # TEMP
        return 54
    # Winter
    elif cur_semester == 2:
        return 54
    # Sprint
    else:
        return 54
def get_holidays(cur_semester):
    # Returns a list of the days holidays are on for each respective term
    # Fall
    if cur_semester == 1:
        # TEMP
        return [5, 17, 18, 21, 22, 23, 24, 30]
    # Winter
    elif cur_semester == 2:
        return [5, 17, 18, 21, 22, 23, 24, 30]
    # Sprint
    else:
        return [5, 17, 18, 30]