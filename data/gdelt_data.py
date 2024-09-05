import requests
from urllib.parse import urlencode


class GDELT:

    def __init__(self):
        self.BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'GDELT Client v2.0'})

    def gdelt_request(self, **kwargs):

        accepted_params = [
            "query", "mode", "startdatetime", "enddatetime", "maxrecords"
        ]

        if not all(i in accepted_params for i in kwargs):
            raise ValueError(f"Incorrect param definition. Options are {accepted_params}")

        params = {"mode": "tonechart", "format": "json"}
        params.update(kwargs)

        if kwargs:
            params.update(kwargs)

        r = requests.get(self.BASE_URL, params=params)

        return r.json()




