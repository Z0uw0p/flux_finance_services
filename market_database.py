import yfinance as yf
from utils import *
import schedule
import time

engine = create_engine('flux-finance:northamerica-northeast1:flux-finance-market-database')

sec_ticker_list = pd.read_csv(r"ticker_lists\sec_tickers.csv")['Ticker'].to_list()
tse_ticker_list = pd.read_csv(r"ticker_lists\tse_tickers.csv")['Ticker'].to_list()
ticker_list = tse_ticker_list + sec_ticker_list

initialize_database(ticker_list)

schedule.every().day.at("19:00").do(daily_update, ticker_list)

while True:
    schedule.run_pending()
    time.sleep(1)
