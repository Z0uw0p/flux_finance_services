import logging
from sqlalchemy import create_engine
import os
import yfinance as yf
import pandas as pd

# Fetch stock data
def fetch_stock_data(ticker, period):

    try:
        data = yf.download(ticker, period)
        
        if data.empty:
            
            return None
        
        return data
    
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")

        return None

# Calculate the EMA
def calculate_ema(data, window):
    
    return data['Close'].ewm(span=window, adjust=False).mean()

# Calculate the MACD
def calculate_macd(data, fast_legnth, slow_length, signal_length):
    ema_fast = calculate_ema(data, fast_legnth)
    ema_slow = calculate_ema(data, slow_length)
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal_length, adjust=False).mean()
    macd_histogram = macd - macd_signal

    return macd, macd_signal, macd_histogram

# Calculate the Impulse MACD using the ZLEMA
def calculate_impulse_macd(data, fast_length, slow_length, signal_smma, price_col='Close'):

    if price_col not in data.columns:

        raise ValueError(f"Column '{price_col}' not found in data")
    
    zlema_fast = calc_zlema(data['Close'], fast_length)
    zlema_slow = calc_zlema(data['Close'], slow_length)
    impulse_macd = zlema_fast - zlema_slow
    impulse_macd_signal = calc_smma(impulse_macd, signal_smma)
    impulse_macd_histogram = impulse_macd - impulse_macd_signal
    
    return impulse_macd, impulse_macd_signal, impulse_macd_histogram

# Calculate the RSI
def calculate_rsi(series, period):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 +rs))
    
    return rsi

# Calculate Volatility
def calculate_volatility(series, period):
    
    return series.pct_change().rolling(window=period).std()

# Calculate Volume
def calculate_volume(data):
    
    return data['Volume']

# Calculate SMMA
def calc_smma(series, length):
    smma = series.ewm(alpha=1/length, adjust=False).mean()
    
    return smma

# Calculate ZLEMA
def calc_zlema(series, length):
    ema1 = series.ewm(span=length, adjust=False).mean()
    ema2 = ema1.ewm(span=length, adjust=False).mean()
    d = ema1 - ema2
    
    return ema1 + d

def setup_market_data_database():
    conn = sqlite3.connect('market_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                date DATE NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                ema_30 REAL,
                ema_50 REAL,
                ema_80 REAL,
                macd REAL,
                macd_signal REAL,
                macd_histogram REAL,
                impulse_macd REAL,
                impulse_macd_signal REAL,
                impulse_macd_histogram REAL,
                rsi_14 REAL,
                volatility REAL,
                smma_9 REAL,
                smma_20 REAL,
                zlema_12 REAL,
                zlema_26 REAL,
                UNIQUE(ticker, date)
                )
    ''')

    conn.commit()
    conn.close()

async def fetch_and_store_market_data(ticker, period):
    logging.info(f'Starting to fetch and store data for {ticker}')

    periods_to_try = ["10y", "5y", "2y", "1y", "6mo", "3mo", "1mo"]
    
    for p in periods_to_try:
    # Fetch historical data
        try:
            logging.info(f"Attempting to fetch {p} data for {ticker}")
            data = yf.Ticker(ticker).history(period=p)

            if data.empty:
                logging.warning(f'No data found for {ticker} with period {p}, trying shorter period.')

                continue

            # Calculate indicators
            # EMAs
            data['ema_30'] = calculate_ema(data, 30)
            data['ema_50'] = calculate_ema(data, 50)
            data['ema_80'] = calculate_ema(data, 80)
            # MACD
            data['macd'], data['macd_signal'], data['macd_histogram'] = calculate_macd(data)
            # ZLEMAs
            data['zlema_12'] = calc_zlema(data['Close'], 12)
            data['zlema_26'] = calc_zlema(data['Close'], 26)
            # Impulse MACD
            data['impulse_macd'], data['impulse_macd_signal'], data['impulse_macd_histogram'] = calculate_impulse_macd(data)
            # RSI
            data['rsi_14'] = calculate_rsi(data['Close'], 14)
            # Volatility
            data['volatility'] = calculate_volatility(data['Close'], 30)
            # Volume
            data['volume'] = calculate_volume(data)
            # SMMAs
            data['smma_9'] = calc_smma(data['Close'], 9)
            data['smma_20'] = calc_smma(data['Close'], 20)

            logging.info(f'Successfully fetched and stored data for {ticker} with period {p}')

            return

        except Exception as e:
            logging.error(f'Error fetching and storing data for {ticker} with period {p}: {str(e)}')
    
    logging.error(f'Failed to fetch any data for {ticker} across all periods.')

# Connect to Google Cloud SQL
def connect_to_cloud_sql(user, password, host, database):
    
    try:
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

        return engine
    
    except Exception as e:
        logging.error(F"Error connecting to the database: {str(e)}")

        return None
    
def save_to_sql(data, ticker, engine):
    try:
        data.to_sql(ticker, engine, if_exists='replace', index=True)
        logging.info(f"Data for {ticker} saved successfully!")

    except Exception as e:
        logging.error(f"Error saving data for {ticker}: {str(e)}")

def fetch_and_store_stocks(stock_list, user, password, host, database):
    engine = connect_to_cloud_sql(user, password, host, database)

    if engine is None:
        
        return
    
    periods = ["10y", "5y", "2y", "1y", "6mo", "3mo", "1mo"]

    for ticker in stock_list:

        for period in periods:

            data = fetch_stock_data(ticker, period)

            if data is not None:
                save_to_sql(data, ticker, engine)

                break
