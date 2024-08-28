
import pandas as pd
import yfinance as yf


def get_stock_historical(ticker: str, period: str = "1y", interval: str = "1d"):

    spx_data = yf.download(ticker, period=period, interval=interval)

    spx_df = spx_data[['Open', 'Close']].reset_index()

    spx_df.columns = ['date', 'spx_open', 'spx_close']

    spx_df['date'] = pd.to_datetime(spx_df['date'])

    return spx_df






