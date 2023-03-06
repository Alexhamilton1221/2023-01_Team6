

def get_term_length(term):
    # Gets the length of a term (INCLUDING HOLIDAYS)
    if term == 1:
        # TEMP
        return 48
    # Winter
    elif term == 2:
        return 52
    # Sprint
    else:
        return 50
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