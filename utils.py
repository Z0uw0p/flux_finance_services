import yfinance as yf
import pandas as pd
import os
import logging
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

# Set up logging
def setup_logging(level):

    if level == "info":
        logging.basicConfig(level=logging.INFO)

    else:
        logging.basicConfig(level=logging.DEBUG)

# Fetch historical data from Yahoo Finance
def fetch_historical_data(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval)
    logging.info(f"Data fetched for {ticker}, for a {period} period, with a {interval} interval")

    return data

# Fetch daily data from Yahoo Finance
def fetch_daily_data(ticker):
    data = yf.download(ticker, period='1d')
    logging.info(f"Data fetched for {ticker} for the last day")

    return data

# Get environment variables
def get_env_var(var):
    variable = os.getenv(var)

    if variable is None:

        raise ValueError(f"Environment variable {var} is not set")
    
    else:
        logging.info(f"Environment variable {var} is set")

    return variable

# Get the database connection
def get_conn(conn_name, username, password, db_name) -> pymysql.connections.Connection:
    connector = Connector()
    
    conn: pymysql.connections.Connection = connector.connect(
        conn_name,
        "pymysql",
        user=username,
        password=password,
        db=db_name,
    )

    logging.info(f"Connected to {db_name} database")

    return conn
