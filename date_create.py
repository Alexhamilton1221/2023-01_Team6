from calendar import Calendar

#Date create example:
# Calendar1 = DateCreate(2023,"Fall")
# Calendar1.Calendar_dictionary -> returns the dictionary of dicationaries for the dates
# if you want to add holidays manually, use the format yyyy-mm-dd with Calendar1.add_holidays("2023-09-01")
#
# Days that have None, do not have lectures. All other days have integer based on the class day for the schedule

#create_date_dict() helper function to return date dictionary
def create_date_dict(year,semester):
    date_create_obj = DateCreate(year, semester)
    return date_create_obj.calendar_dictionary

class DateCreate:
    def __init__(self, year, term):
        self.calendar_dictionary = {}
        self.year = year
        self.term = term
        self.term_start = 0
        self.start_day = 0
        #Holidays and reading weeks from Fall 2022 to Spring 2024
        self.holidays = ['2022-09-07','2022-10-10','2022-11-07','2022-11-08','2022-11-09','2022-11-10','2022-11-11','2022-12-25','2023-01-2','2023-02-20','2023-02-21','2023-02-22','2023-02-23','2023-02-24','2023-04-7','2023-04-10','2023-05-22','2023-07-3','2023-08-07','2023-09-04','2023-10-09','2023-11-13','2023-11-14','2023-11-15','2023-11-16','2023-11-17','2023-12-25','2024-01-01','2024-02-19','2023-11-20','2023-11-21','2023-11-22','2023-11-23','2024-03-29','2024-04-01','2024-05-20','2024-07-01','2024-08-05']
        # generating the day dictionaries within the month dictionaries
        self.generate_calendar()

        self.first_month = list(self.calendar_dictionary.keys())[0]
        self.start_day = self.locate_start_day()
        self.insert_class_days()

        #return self.calendar_dictionary

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

        lecture_day_counter = 1
        day_counter = 1

        first_day = self.first_class_day()

        for month in self.calendar_dictionary:
            for date in self.calendar_dictionary[month]:
                if first_day < day_counter:
                    if (weekday in (1, 2, 3, 4)) and date not in self.holidays:
                        self.calendar_dictionary[month][date] = lecture_day_counter
                        lecture_day_counter += 1

                if weekday == 7:
                    weekday = 1
                else:
                    weekday += 1

                day_counter += 1
        return None

    def locate_start_day(self):
        month = self.first_month
        start_day = 0

        for i in Calendar().itermonthdates(self.year, month):
            start_day += 1
            output_month = int(str(i).split("-")[1])

            if output_month == month:
                return start_day

    def labor_day_calc(self):
        # first wednesday after first monday of september
        weekday = self.start_day
        monday_check = 0

        loop_counter = 1
        while (weekday != 3) and (monday_check != 1):
            if weekday == 1:
                monday_check = 1

            if weekday == 7:
                weekday = 1
            else:
                weekday += 1

            loop_counter += 1
        return loop_counter

    def winter_day_calc(self):
        # first wednesday after January 1st
        weekday = self.start_day
        loop_counter = 0

        while weekday != 3:

            if weekday == 7:
                weekday = 1
            else:
                weekday += 1
            loop_counter += 1

        return loop_counter

    def first_class_day(self):
        if self.first_month == 9:
            return self.labor_day_calc()
        elif self.first_month == 1:
            return self.winter_day_calc()
        else:
            # if it is spring, starts on May 1st or first monday after May 1st
            return 0
    def add_holidays(self, holiday):
        self.holidays.append(holiday)
        return None


