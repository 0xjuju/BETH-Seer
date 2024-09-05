from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf


def get_interest_rate_changes(tickers: list[str], days: int = 365):

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    interest_rates_df = pd.DataFrame()

    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        data['Ticker'] = ticker
        interest_rates_df = interest_rates_df.append(data)

    interest_rates_df = interest_rates_df.reset_index()
    interest_rates_df = interest_rates_df[['Date', 'Ticker', 'Close']]

    return interest_rates_df


def get_stock_historical(ticker: str, period: str = "1y", interval: str = "1d"):

    spx_data = yf.download(f"^{ticker}", period=period, interval=interval)

    spx_df = spx_data[['Open', 'Close']].reset_index()

    spx_df.columns = ['date', 'spx_open', 'spx_close']

    spx_df['date'] = pd.to_datetime(spx_df['date'])

    return spx_df






