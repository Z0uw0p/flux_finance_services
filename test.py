import yfinance as yf

data = yf.download('AAPL', period='mo', interval='4d')