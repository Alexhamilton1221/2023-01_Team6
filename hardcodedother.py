

def get_term_length(term):
    # Gets the length of a term (INCLUDING HOLIDAYS)
    # Shifted by 2 to accomodate starting on a wendsday
    if term == 1:
        # TEMP
        return 54
    # Winter
    elif term == 2:
        return 54
    # Sprint
    else:
        return 54
def get_holidays(term):
    # Returns a list of the days holidays are on for each respective term
    # Fall
    if term == 1:
        # TEMP
        return [5, 17, 18, 21, 22, 23, 24, 30]
    # Winter
    elif term == 2:
        return [5, 17, 18, 21, 22, 23, 24, 30]
    # Sprint
    else:
        return [5, 17, 18, 30]