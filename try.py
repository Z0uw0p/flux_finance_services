import yfinance as yf
import pandas as pd

# Define the stock ticker
sec_ticker_list = pd.read_csv(r"ticker_lists\sec_tickers.csv")
tse_ticker_list = pd.read_csv(r"ticker_lists\sec_tickers.csv")

ticker_list = sec_ticker_list['Ticker'].tolist() + tse_ticker_list['Ticker'].tolist()

for ticker in ticker_list:
    # Fetch the ticker information
    stock = yf.Ticker(ticker)
    info = stock.info

    # Retrieve the relevant information
    company_name = info.get("longName", "N/A")
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    market_cap = info.get("marketCap", "N/A")
    current_price = info.get("currentPrice", "N/A")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh", "N/A")
    fifty_two_week_low = info.get("fiftyTwoWeekLow", "N/A")
    dividend_yield = info.get("dividendYield", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")
    eps = info.get("trailingEps", "N/A")
    description = info.get("longBusinessSummary", "Description not found")

    # Write the information to a markdown file
    file_name = f"ticker_description/{ticker}.md"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"# {company_name} ({ticker})\n\n")
        file.write(f"**Sector:** {sector}\n\n")
        file.write(f"**Industry:** {industry}\n\n")
        file.write(f"**Market Cap:** {market_cap}\n\n")
        file.write(f"**Current Price:** {current_price}\n\n")
        file.write(f"**52-Week High:** {fifty_two_week_high}\n\n")
        file.write(f"**52-Week Low:** {fifty_two_week_low}\n\n")
        file.write(f"**Dividend Yield:** {dividend_yield}\n\n")
        file.write(f"**P/E Ratio:** {pe_ratio}\n\n")
        file.write(f"**EPS:** {eps}\n\n")
        file.write(f"**Description:**\n\n{description}\n")
