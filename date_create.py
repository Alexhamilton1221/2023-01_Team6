from calendar import Calendar


class DateCreate:
    def __init__(self, year, term):
        self.calendar_dictionary = {}
        self.year = year
        self.term = term
        self.term_start = 0
        self.start_day = 0

        #generating the day dictionaries within the month dictionaries
        self.generate_calendar()
        self.start_day = self.locate_start_day()

    def generate_calendar(self):
        months = []
        # fall term
        if self.term == "Fall":
            months = [9, 10, 11, 12]
        # winter term
        elif self.term == "Winter":
            months = [1, 2, 3, 4]
        # spring/summer term
        elif self.term == "Spring":
            months = [5, 6, 7, 8]

        for i in months:
            self.calendar_dictionary[i] = self.month_dictionary(self.year, i)
        return self.calendar_dictionary

    def month_dictionary(self, year, month):
        month_dict = {}

        for i in Calendar().itermonthdates(year, month):
            outputMonth = int(str(i).split("-")[1])

            if outputMonth == int(month):
                month_dict[str(i)] = None
        return month_dict

    def insert_class_days(self):
        weekday = self.start_day
        day_counter = 1
        for month in self.calendar_dictionary:
            for date in self.calendar_dictionary[month]:
                if weekday in (1,2,3,4) :
                    self.calendar_dictionary[month][date] = day_counter
                    day_counter += 1

                if weekday == 7:
                    weekday = 1
                else:
                    weekday += 1
        print(self.calendar_dictionary)
        return None

    def locate_start_day(self):
        first_month = list(self.calendar_dictionary.keys())[0]
        start_day = 0

        for i in Calendar().itermonthdates(self.year, first_month):
            start_day += 1
            output_month = int(str(i).split("-")[1])

            if output_month == first_month:
                return start_day