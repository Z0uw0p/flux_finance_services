from utils import *

tse_ticker_list = pd.read_csv(r"ticker_lists\tse_tickers.csv")['Ticker'].to_list()
sec_ticker_list = pd.read_csv(r"ticker_lists\sec_tickers.csv")['Ticker'].to_list()

ticker_list = tse_ticker_list + sec_ticker_list

user = "flux-finance-market-database"
password = 'f8v7#P6nbe"x9.1T'
host = ""
database = ""