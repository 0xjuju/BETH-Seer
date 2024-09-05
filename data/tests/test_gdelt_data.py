from django.test import TestCase
from data.gdelt_data import GDELT


class GDELTGKGTestCase(TestCase):
    def setUp(self):
        self.client = GDELT()

    def test_gdelt_request(self):

        res = self.client.gdelt_request(
            query="bitcoin",
            startdatetime="20230901000000",
            enddatetime="20240901000000",
            maxrecords=10
        )

        print(res)





