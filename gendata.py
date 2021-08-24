import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
from datetime import datetime


def get_investment_returns_data(ticker):

    # Get the data for the stock AAPL
    ticker = 'SPY QQQ'
    startDate = '2000-01-06'
    endDate = datetime.now().strftime("%Y-%m-%d")
    data = yf.download(ticker,startDate, endDate, interval = "1wk")
    strDate = ""
    currentHolding = 0
    cumulativeCost = 0.0
    currentPortfolioValue = 0.0
    averageCost = 0.0
    currentPrice = 0.0
    # print(data)

    # print("Date", "CurrentHolding", "CurrentPrice", "AveragePrice", "CumulativeCost", "CurrentPortfolioValue", "Profit/Loss")
    portfolioData = []
    for i, row in data.iterrows():
        if math.isnan(row['Open'][0]) == False:
            datetime_object = i.to_pydatetime()
            strDate = datetime_object.strftime("%Y-%m-%d")
            currentHolding += 1
            datetime_object = i.to_pydatetime()
            strDate = datetime_object.strftime("%Y-%m-%d")
            #sum(row['Open']) gives the sum of price for all tickers
            currentPrice = float(sum(row['Open']))
            cumulativeCost = cumulativeCost + currentPrice
            currentPortfolioValue = currentHolding * currentPrice
            averageCost = cumulativeCost/currentHolding
            mytuple = (strDate, currentHolding, currentPrice, averageCost, cumulativeCost, currentPortfolioValue, currentPortfolioValue-cumulativeCost)
            portfolioData.append(mytuple)
            # print(mytuple)

    df = pd.DataFrame(portfolioData, columns=["Date", "CurrentHolding", "CurrentPrice", "AveragePrice", "CumulativeCost", "CurrentPortfolioValue", "Profit/Loss"])

    profitPercentage = (currentPortfolioValue-cumulativeCost)/cumulativeCost*100

    rcParams['figure.figsize'] = 14,8
    x = df['Date']
    plt.plot(x, df['CumulativeCost'], label='CumulativeCost')
    plt.plot(x, df['CurrentPortfolioValue'], label='CurrentPortfolioValue')
    # plt.grid(True, color='k', linestyle=':')
    plt.title('Weekly Investment - 10 Year Returns')
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Price in $")
    plt.xticks(x[::20],  rotation='vertical')
    plt.tight_layout()
    plt.style.use('ggplot')
    summary = """
    If you bought one stock of [%s] every week from %s to %s\n
    Total Investment: $%.2f\n
    Portfolio Value : $%.2f\n
    Profit / Loss   : $%.2f\n
    Profit Percent  : %.2f\n
    Average Cost    : %.2f\n
    Current Price   : %.2f\n
    Current Holding : %d\n
    """ % (ticker, startDate, endDate, cumulativeCost, currentPortfolioValue, currentPortfolioValue-cumulativeCost, profitPercentage, averageCost, currentPrice, currentHolding)
    print(summary)
    plt.text(1, cumulativeCost, summary)
    return df, plt.figure(1)

    # plt.savefig(ticker + ".png")
    # plt.show()
