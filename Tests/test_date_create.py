from unittest import TestCase
from date_create import DateCreate


class TestDateCreate(TestCase):
    def test_dictionary_generate(self):
        date1 = DateCreate(2023,"Fall")
        #print(date1.generate_calendar())
        #assert date1 != True

    def test_month_dict_generate(self):
        date2 = DateCreate(2023,"Fall")
        #print(date2.month_dictionary(2023,9))

    def test_insert_class_days(self):
        date3 = DateCreate(2023,"Fall")
        #date3.generate_calendar()
        #date3.insert_class_days()

    def test_locate_start_day(self):
        date4 = DateCreate(2023,"Fall")
        date4.locate_start_day()

    def test_lobor_day_calc(self):
        date5 = DateCreate(2023,"Fall")
        date5.insert_class_days()

    def test_winter_day_calc(self):
        date6 = DateCreate(2023, "Winter")
        date6.insert_class_days()
    def test_spring_day_calc(self):
        date7 = DateCreate(2023, "Spring")
        date7.insert_class_days()
        print(date7.calendar_dictionary)




