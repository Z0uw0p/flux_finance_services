### GCP_flux_finance
Flux Finance project over the GCP

## [[Market Database]]:
Instance of a Cloud SQL over on the GCP. It stores the daily market data of each stock in the ticker list up to 10 years. For the stocks that have not been listed on the yfinance API for 10 years, it has stored the data for the longest possible period. Everyday, the data will be updated with the latest changes.
    - ***Database Columns***:
        - ID
        - TICKER
        - DATE
        - OPEN
        - HIGH
        - LOW
        - CLOSE
        - VOLUME
        - EMA 20
        - EMA 50
        - EMA 80
        - MACD
        - MACD SIGNAL
        - MACD HISTOGRAM
        - IMPULSE MACD
        - IMPULSE MACD SIGNAL
        - IMPULSE MACD HISTOGRAM
        - RSI 14
        - VOLATILITY
        - SMMA 9
        - SMMA 20
        - ZLEMA 12
        - ZLEMA 16
    - **fetch_historical_data(ticker, period, ,interval)**:
        - *ticker*: Stock's symbol
        - *period*: Period must be one of: ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        - *interval*: Interval must be one of: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
    - **fetch_daily_data(ticker)**:
        - *ticker*: Stock's symbol
    - **append_historical_data_to_market_db(data)**:
        - *data*: Database fetched with **fetch_historical_data()**
    - **append_daily_data_to_market_db(data)**:
        - *data*: Database fetched with **fetch_daly_data()**
    
## [[Zara Nexus]]:
Instance of a VM over on the GCP. It is tasked with filling the [[Market Database]] with the daily data over the maximum period for each stock in the ticker list.