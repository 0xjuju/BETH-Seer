
from data.technical_analysis import *
from django.test import TestCase
import pandas as pd


class TestTechAnalysis(TestCase):

    def setUp(self):
        pass

    def test_estimate_ta_nan(self):
        df = get_ta_indicators()
        estimate_nan_values = estimate_ta_nan()

    def test_get_ta_indicators(self):
        ta_ind = get_ta_indicators()

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print(ta_ind)




