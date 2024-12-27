import sqlite3
import pandas as pd
import ta

# Function to load data from SQLite
def load_data_from_db(db_name="mse_data.db", ticker_code="ADIN"):
    """
    Load data for a specific ticker from the SQLite database.
    """
    connection = sqlite3.connect(db_name)
    query = f"""
    SELECT date, last_price AS Last_Trade_Price, max_price AS Max, min_price AS Min, volume AS Volume
    FROM mse_data
    WHERE ticker_code = '{ticker_code}'
    ORDER BY date ASC
    """
    df = pd.read_sql_query(query, connection)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    connection.close()
    return df


# Function to calculate technical indicators
def calculate_indicators(df):
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Last_Trade_Price']).rsi()
    df['Stochastic'] = ta.momentum.StochasticOscillator(
        high=df['Max'], low=df['Min'], close=df['Last_Trade_Price']
    ).stoch()
    df['MACD'] = ta.trend.MACD(close=df['Last_Trade_Price']).macd()
    df['Momentum'] = df['Last_Trade_Price'].diff()
    df['CCI'] = ta.trend.CCIIndicator(
        high=df['Max'], low=df['Min'], close=df['Last_Trade_Price']
    ).cci()
    df['SMA'] = ta.trend.SMAIndicator(close=df['Last_Trade_Price'], window=14).sma_indicator()
    df['EMA'] = ta.trend.EMAIndicator(close=df['Last_Trade_Price'], window=14).ema_indicator()
    df['WMA'] = df['Last_Trade_Price'].rolling(window=14).apply(
        lambda x: (x * range(1, len(x) + 1)).sum() / sum(range(1, len(x) + 1))
    )
    df['MAE_upper'], df['MAE_lower'] = df['SMA'] * 1.02, df['SMA'] * 0.98
    df['HMA'] = ta.trend.WMAIndicator(close=df['Last_Trade_Price'], window=14).wma()
    return df


# Function to generate buy/sell signals
def generate_signals(df):
    df['RSI_signal'] = df['RSI'].apply(lambda x: 'Buy' if x < 30 else 'Sell' if x > 70 else 'Hold')
    df['MA_signal'] = df.apply(
        lambda row: 'Buy' if row['SMA'] < row['EMA'] else 'Sell' if row['SMA'] > row['EMA'] else 'Hold', axis=1
    )
    df['MACD'] =df['MACD'].apply(lambda x: 'Buy' if x>0 else 'Sell' if x<0 else 'Hold')
    df['CCI'] = df['CCI'].apply(lambda x: 'Sell' if x > 100 else 'Buy' if x<-100 else 'Hold')
    df.loc[df['CCI'] < -100, 'signal'] = 'Buy'

    return df


# Function to aggregate signals
def collect_signals(df):
    signals = ['RSI_signal', 'MA_signal', 'MACD_signal', 'CCI_signal']
    df['Overall_signal'] = df[signals].mode(axis=1)[0]  # Most frequent signal
    return df


# Needs to be connected to the main
