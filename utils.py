import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

def fetch_historical_data(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval)

    return data

def fetch_daily_data(ticker):
    data = yf.download(ticker, period='1d')

    return data

def append_historical_data_to_market_db(data, ticker):
    data.to_sql('historical_data', engine, if_exists='append', index=False)

def append_daily_data_to_market_db(data, ticker):
    data.to_sql('daily_data', engine, if_exists='append', index=False)

def initialize_database(tickers):
    
    for ticker in tickers:
        data = fetch_historical_data(ticker, 'max', '1d')
        append_historical_data_to_market_db(data, ticker)

def daily_update(tickers):

    for ticker in tickers:
        data = fetch_daily_data(ticker)
        append_daily_data_to_market_db(data, ticker)