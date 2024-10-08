import os
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from google.cloud.sql.connector import Connector
import schedule
import time
from utils import *

# Initialize the Cloud SQL connection
connector = Connector()

# Function to create a connection to the Cloud SQL instance
def getconn():
    conn = connector.connect(
        os.getenv("MARKET_DATABASE_NAME"),
        "pymysql",
        user=os.getenv("MARKET_DATABASE_USER"),
        passwoed=os.getenv("MARKET_DATABASE_PASSWORD"),
    )

    return conn

# Create the engine
engine = create_engine("mysql+pymysql://", creator=getconn)

sec_ticker_list = pd.read_csv('sec_ticker_list.csv')["Ticker"].tolist()
tse_ticker_list = pd.read_csv('tse_ticker_list.csv')['Ticker'].tolist()
ticker_list = sec_ticker_list + tse_ticker_list

initialize_database(ticker_list)

schedule.every().day.at("19:00").do(daily_update, ticker_list)

while True:
    schedule.run_pending()
    time.sleep(1)