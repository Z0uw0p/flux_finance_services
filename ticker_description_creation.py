import yfinance as yf
import pandas as pd

# Define the stock ticker
sec_ticker_list = pd.read_csv(r"ticker_lists\sec_tickers.csv")
tse_ticker_list = pd.read_csv(r"ticker_lists\sec_tickers.csv")

#sec_and_tse_ticker_list = sec_ticker_list['Ticker'].tolist() + tse_ticker_list['Ticker'].tolist()
portfolio_ticker_list = ["SIA.TO"]
ticker_list = portfolio_ticker_list
total_tickers = len(ticker_list)
not_found_list = []

for index, ticker in enumerate(ticker_list):
    # Ensure the ticker is a string
    ticker = str(ticker)

    try:
        # Fetch the ticker information
        stock = yf.Ticker(ticker)
        info = stock.info

        # Retrieve the relevant information
        company_name = info.get("longName", "N/A")
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        market_cap = info.get("marketCap", "N/A")
        if market_cap != "N/A":
            market_cap = f"{market_cap:,}"
        current_price = info.get("currentPrice", "N/A")
        if current_price != "N/A":
            current_price = f"{current_price:.2f}"
        fifty_two_week_high = info.get("fiftyTwoWeekHigh", "N/A")
        if fifty_two_week_high != "N/A":
            fifty_two_week_high = f"{fifty_two_week_high:.2f}"
        fifty_two_week_low = info.get("fiftyTwoWeekLow", "N/A")
        if fifty_two_week_low != "N/A":
            fifty_two_week_low = f"{fifty_two_week_low:.2f}"
        dividend_yield = info.get("dividendYield", "N/A")
        if dividend_yield != "N/A":
            dividend_yield = f"{dividend_yield * 100:.2f}%"
        pe_ratio = info.get("trailingPE", "N/A")
        if pe_ratio != "N/A":
            pe_ratio = f"{float(pe_ratio):.2f}"
        eps = info.get("trailingEps", "N/A")
        if eps != "N/A":
            eps = f"{float(eps):.2f}"
        description = info.get("longBusinessSummary", "Description not found")

        if company_name == "N/A":
            not_found_list.append(ticker)

        # Write the information to a markdown file
        file_name = f"ticker_description/{ticker}.md"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write("---\n")
            file.write(f"title: {company_name} ({ticker})\n")
            file.write(f"sector: {sector}\n")
            file.write(f"industry: {industry}\n")
            file.write(f"market_cap: {market_cap}\n")
            file.write(f"current_price: {current_price}\n")
            file.write(f"fifty_two_week_high: {fifty_two_week_high}\n")
            file.write(f"fifty_two_week_low: {fifty_two_week_low}\n")
            file.write(f"dividend_yield: {dividend_yield}\n")
            file.write(f"pe_ratio: {pe_ratio}\n")
            file.write(f"eps: {eps}\n")
            file.write("---\n\n")
            file.write(f"# {company_name} ({ticker})\n\n")
            file.write(f"**Sector:** {sector}\n\n")
            file.write(f"**Industry:** {industry}\n\n")
            file.write(f"**Market Cap:** ${market_cap}\n\n")
            file.write(f"**Current Price:** ${current_price}\n\n")
            file.write(f"**52-Week High:** ${fifty_two_week_high}\n\n")
            file.write(f"**52-Week Low:** ${fifty_two_week_low}\n\n")
            file.write(f"**Dividend Yield:** {dividend_yield}\n\n")
            file.write(f"**P/E Ratio:** {pe_ratio}\n\n")
            file.write(f"**EPS:** {eps}\n\n")
            file.write(f"**Description:**\n\n{description}\n")

        print(f"Description for {ticker} created successfully. {total_tickers - index - 1} tickers remaining.")

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        not_found_list.append(ticker)

print(f"Description for all tickers done. The following's data was not found: {not_found_list}")
