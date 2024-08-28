from datetime import datetime, timedelta

from coinbase.rest import RESTClient
import decouple
import pandas as pd


class CBApi:
    def __init__(self):
        self.API_KEY = decouple.config("COINBASE_API_KEY")
        self.API_SECRET = decouple.config("COINBASE_API_SECRET")
        self.client = RESTClient(api_key=self.API_KEY, api_secret=self.API_SECRET)

    @staticmethod
    def _verify_granularity(func):
        def wrapper(*args, **kwargs):
            accepted_granularity = [
                "UNKNOWN_GRANULARITY", "ONE_MINUTE", "FIVE_MINUTE", "FIFTEEN_MINUTE", "THIRTY_MINUTE", "ONE_HOUR",
                "TWO_HOUR", "SIX_HOUR", "ONE_DAY"
            ]
            granularity = kwargs["granularity"]
            if granularity not in accepted_granularity:
                print(granularity, " Not valid")
                raise ValueError(f"{granularity} Not a valid option from list: {accepted_granularity}")

            return func(*args, **kwargs)

        return wrapper

    @_verify_granularity
    def get_prices(self, token: str, granularity: str, days: int = 350):

        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        candles = self.client.get_candles(
            product_id=token,
            start=int(start_time.timestamp()),
            end=int(end_time.timestamp()),
            granularity=granularity
        )

        df = pd.DataFrame([
            {
                "date": candle["start"],
                "open": float(candle["open"]),
                "close": float(candle["close"]),
                "high": float(candle["high"]),
                "low": float(candle["low"])
            } for candle in candles["candles"]
        ])

        df['date'] = pd.to_datetime(df['date'], unit="s")
        df.set_index('date', inplace=True)

        return df

    @_verify_granularity
    def get_volume(self, token: str, granularity: str, days: int = 350):

        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        candles = self.client.get_candles(
            product_id=token,
            start=int(start_time.timestamp()),
            end=int(end_time.timestamp()),
            granularity=granularity
        )

        df = pd.DataFrame([
            {
                "date": candle["start"],
                "volume": float(candle["volume"]),
            } for candle in candles["candles"]
        ])

        df['date'] = pd.to_datetime(df['date'], unit="s")
        df.set_index('date', inplace=True)

        return df




