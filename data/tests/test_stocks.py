
from data.stocks import *
from django.test import TestCase


class TestStocks(TestCase):
    def setUp(self):
        pass

    def test_get_interest_rate_changes(self):
        res = get_interest_rate_changes([""], days=365)

    def test_get_stock_historical(self):

        res = get_stock_historical(ticker="GSPC")
        print(res)





