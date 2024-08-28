
from collections import defaultdict
from datetime import datetime
import os
from typing import Any, Union

from data.models import BTCArticle
from google.cloud import bigquery
from google.cloud.bigquery import table
import pandas as pd


class BigQuery:

    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud_credentials.json"
        self.client = bigquery.Client()

    def _make_query(self, query: str, query_params: list[bigquery.ScalarQueryParameter] = None):
        if query_params:
            job_config = bigquery.QueryJobConfig(query_parameters=query_params)
            query_job = self.client.query(query, job_config=job_config)
        else:
            query_job = self.client.query(query)

        return query_job.result()

    @staticmethod
    def df_to_database(df: pd.DataFrame) -> None:
        to_dict = df.to_dict(orient="records")
        upload_list = [BTCArticle(**article) for article in to_dict]
        BTCArticle.objects.bulk_create(upload_list)


    @staticmethod
    def format_gkg_data(data_table: table.RowIterator) -> pd.DataFrame:
        """
        :param data_table:
        :return: Dataframe containing gkg article data_dd
        """

        dataframe = pd.DataFrame(
            columns=[
                "document_id", "themes", "tone", "positive_score", "negative_score", "polarity",
                "activity_reference_density", "magnitude", "persons", "organizations", "date_created",
            ]
        )

        for row in data_table:
            document_id = row[0]
            themes = row[1]
            tone = row[2]
            tone = tone.split(",")
            persons = row[3]
            organizations = row[4]
            article_date = row[5]

            r = [document_id, themes, tone[0], tone[1], tone[2], tone[3], tone[4], tone[5], persons, organizations,
                 article_date]

            dataframe.loc[len(dataframe)] = r

        return dataframe

    @staticmethod
    def format_extracted_gkg_data(dataset: defaultdict[Any, list], max_take=None) -> pd.DataFrame:
        """

        :param dataset: List of article by date
        :param max_take: Max number of articles to extract from each day
        :return: Same dataset but sort the articles by their magnitude value
        """

        for key, articles in dataset.items():
            data = sorted(articles, key=lambda i: i["tone"]["magnitude"], reverse=True)

            if max_take:
                dataset[key] = data[0:max_take]
            else:
                dataset[key] = data

        dataset = pd.DataFrame(dataset)

        return dataset

    def gdelt_gkg(self, start_date: datetime, end_date: datetime, keyword: str, limit: int, offset: int = 0) -> table.RowIterator:
        date_format = "%Y%m%d%H%M%S"
        start_date = datetime.strftime(start_date, date_format)
        end_date = datetime.strftime(end_date, date_format)

        query = """
            SELECT 
                DocumentIdentifier,
                V2Themes,
                V2Tone,
                V2Persons,
                V2Organizations,
                DATE(PARSE_TIMESTAMP('%Y%m%d%H%M%S', CAST(DATE AS STRING))) AS date
            FROM
                `gdelt-bq.gdeltv2.gkg`
            WHERE 
                DATE BETWEEN @start_date AND @end_date
                AND LOWER(V2Themes) LIKE CONCAT('%', @keyword, '%')
                
                AND (CAST(SPLIT(V2Tone, ',')[SAFE_OFFSET(3)] AS FLOAT64) > 0.5 
                OR CAST(SPLIT(V2Tone, ',')[SAFE_OFFSET(3)] AS FLOAT64) < -0.5)
                
                AND CAST(SPLIT(V2Tone, ',')[SAFE_OFFSET(5)] AS FLOAT64) > 2.0
            ORDER BY
                DATE DESC
                                                                                          
            LIMIT @limit
            
            OFFSET @offset
           
        """

        query_parameters = [
            bigquery.ScalarQueryParameter("start_date", "INT64", start_date),
            bigquery.ScalarQueryParameter("end_date", "INT64", end_date),
            bigquery.ScalarQueryParameter("keyword", "STRING", keyword),
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
            bigquery.ScalarQueryParameter("offset", "INT64", offset)
        ]

        return self._make_query(query, query_params=query_parameters)

    @staticmethod
    def merge_data(data: list[dict[Any]]):
        master = data[0]

        for each in data[1:]:
            for key, value in each.items():
                master[key] += value

        return master





