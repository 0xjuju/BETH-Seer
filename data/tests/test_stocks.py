
from data.stocks import *
from django.test import TestCase


class TestStocks(TestCase):
    def setUp(self):
        pass

    def test_get_stock_historical(self):

        res = get_stock_historical(ticker="GSPC")
        print(res)





