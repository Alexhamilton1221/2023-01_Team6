from unittest import TestCase
from Database.cohorts import Cohorts
from Database.cohort import Cohort

class TestCohorts(TestCase):
    def test_givenNewCohort_AddCohort_HaveChort(self):
        cohort = Cohort("1101", 1, 1, 24, [])
        cohorts = Cohorts()

        cohorts.add_cohort(cohort)
        gottenCohort = cohorts.cohorts[0]

        assert cohort == gottenCohort



