from collections import defaultdict
from datetime import datetime, timedelta

from data.models import BTCArticle
from data.google_bigquery import (BigQuery)
from django.test import TestCase


class TestBigQuery(TestCase):
    def setUp(self):
        self.client = BigQuery()

    def test_df_to_database(self):
        keyword = "bitcoin"
        start_date = datetime.now() - timedelta(days=3)
        end_date = datetime.now()

        articles = self.client.gdelt_gkg(start_date, end_date, keyword, limit=10)
        formatted_articles = self.client.format_gkg_data(articles)
        self.client.df_to_database(formatted_articles)

        articles = BTCArticle.objects.all()
        print(articles.count())

    def test_format_gkg_data(self):
        dataset = [
            ["link.com", "Theme", "1.0, 2.0, 3.0, 4.0, 5.0, 6.0", "persons", "organizations",
             datetime(year=2023, month=11, day=18)],

            ["other.com", "Theme", "1.2, 2.3, 3.4, 4.5, 5.6, 6.7", "ppp", "org", datetime(year=2021, month=11, day=18)],
        ]

        formatted = self.client.format_gkg_data(dataset)
        print(formatted.head())

    def test_format_extracted_gkg_data(self):
        keyword = "bitcoin"
        start_date = datetime.now() - timedelta(days=3)
        end_date = datetime.now()

        articles = self.client.gdelt_gkg(start_date, end_date, keyword, limit=10)

        articles = self.client.format_extracted_gkg_data(articles)

        df = self.client.format_extracted_gkg_data(articles)
        print(df.head())

    def test_make_query(self):
        # query = (
        #     'SELECT name FROM `bigquery-public-data_dd.usa_names.usa_1910_2013` '
        #     'WHERE state = "TX" '
        #     'LIMIT 10'
        # )
        # print("test query get state names.")
        # rows = self.client._make_query(query)
        # print("end get states")
        pass

    def test_get_bitcoin_articles(self):
        keyword = "bitcoin"
        start_date = datetime.now() - timedelta(days=3)
        end_date = datetime.now()

        articles = self.client.gdelt_gkg(start_date, end_date, keyword, limit=10)

        for article in articles:
            print(f"V2 Tone: {article[2]}")
            print(f"V2 Date: {type(article[5])}")
            print("______________________________")

    def test_merge_data(self):

        d1 = defaultdict(list)
        d1["one"] = [1, 2]
        d2 = {"two": [3, 4]}
        d3 = {"one": [7, 7, 7,]}
        d4 = {"three": [3, 1, 5]}

        merged = self.client.merge_data([d1, d2, d3, d4])
        self.assertEqual(merged["one"], [1, 2, 7, 7, 7])







