from coinbase_api.cb_api import CBApi
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from ta import trend
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands


def estimate_ta_nan(ta_df, sentiment_price_df):

    features = sentiment_price_df[['tone', 'positive_score', 'negative_score', 'polarity', 'magnitude',
                                   'open', 'close', 'low', 'high']].values

    dates = sentiment_price_df['date'].values

    # Regression model for each TA indicator
    ta_columns = ['50_ema', '200_ema', 'rsi', 'macd', 'macd_signal', 'bollinger_high', 'bollinger_low']
    original_nan_locations = {}

    for column in ta_columns:
        # Store the original NaN locations
        original_nan_locations[column] = ta_df[column].isna()

        # Create target vector (exclude NaN)
        target = ta_df[column].values
        valid_indices = ~np.isnan(target)
        x_train = features[valid_indices]
        y_train = target[valid_indices]

        # Fit the regression model
        reg = LinearRegression()
        reg.fit(x_train, y_train)

        # Predict missing values
        x_predict = features[np.isnan(target)]
        ta_df.loc[np.isnan(ta_df[column]), column] = reg.predict(x_predict)

    # Interpolation only on the originally missing TA indicators
    for column in ta_columns:
        ta_df[column].loc[original_nan_locations[column]] = ta_df[column].loc[
            original_nan_locations[column]].interpolate(method='linear')

    # Ensure no NaN values remain
    assert ta_df.isnull().sum().sum() == 0, "There are still NaN values present."

    return ta_df


def get_ta_indicators() -> pd.DataFrame:

    # Get BTC prices data_dd as a DataFrame
    df = CBApi().get_btc_prices(granularity="ONE_DAY")

    df['50_ema'] = trend.EMAIndicator(close=df['close'], window=50).ema_indicator()
    df['200_ema'] = trend.EMAIndicator(close=df['close'], window=200).ema_indicator()
    df['rsi'] = RSIIndicator(close=df['close']).rsi()
    macd = trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    bollinger = BollingerBands(close=df['close'])
    df['bollinger_high'] = bollinger.bollinger_hband()
    df['bollinger_low'] = bollinger.bollinger_lband()

    return df[['50_ema', '200_ema', 'rsi', 'macd', 'macd_signal', 'bollinger_high', 'bollinger_low']]





