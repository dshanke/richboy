import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta, WE

duration=10

def ticker_to_list(ticker):
    return ticker.split()

def get_investment_returns_data(ticker):
    start_date = datetime.now() - relativedelta(years=duration)
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
    mutiticker = ticker_to_list(ticker).__len__() > 1
    # print("Date", "CurrentHolding", "CurrentPrice", "AveragePrice", "CumulativeCost", "CurrentPortfolioValue", "Profit/Loss")
    portfolioData = []
    for i, row in data.iterrows():
        isnan = math.isnan(row['Open'][0]) if mutiticker else math.isnan(row['Open'])
        if isnan == False:
            datetime_object = i.to_pydatetime()
            strDate = datetime_object.strftime("%Y-%m-%d")
            currentHolding += 1
            datetime_object = i.to_pydatetime()
            strDate = datetime_object.strftime("%Y-%m-%d")
            #sum(row['Open'][0]) if multiticker gives the sum of price for all tickers
            currentPrice = float(sum(row['Open'][0])) if mutiticker else float(row['Open'])
            cumulativeCost = cumulativeCost + currentPrice
            currentPortfolioValue = currentHolding * currentPrice
            averageCost = cumulativeCost/currentHolding
            mytuple = (strDate, currentHolding, currentPrice, averageCost, cumulativeCost, currentPortfolioValue, currentPortfolioValue-cumulativeCost)
            portfolioData.append(mytuple)
            # print(mytuple)

    df = pd.DataFrame(portfolioData, columns=["Date", "CurrentHolding", "CurrentPrice", "AveragePrice", "CumulativeCost", "CurrentPortfolioValue", "Profit/Loss"])

    profitPercentage = (currentPortfolioValue-cumulativeCost)/cumulativeCost*100

    # rcParams['figure.figsize'] = 10,6
    x = df['Date']
    fig, ax = plt.subplots(figsize=(10, 6))
    # fig.subplots_adjust(bottom=0.15, left=0.2)
    ax.plot(x, df['CumulativeCost'], label='CumulativeCost')
    ax.plot(x, df['CurrentPortfolioValue'], label='CurrentPortfolioValue')
    # ax.set_xlabel('Date')
    ax.set_ylabel('Price in $')
    y_min, y_max = ax.get_ylim()

    # plt.plot(x, df['CumulativeCost'], label='CumulativeCost')
    # plt.plot(x, df['CurrentPortfolioValue'], label='CurrentPortfolioValue')
    # plt.grid(True, color='k', linestyle=':')
    # plt.grid()
    plt.title('Weekly Investment - 10 Year Returns')
    plt.legend(loc="lower right")
    # plt.xlabel("Date")
    # plt.ylabel("Price in $")
    plt.xticks(x[::20],  rotation='vertical')
    plt.tight_layout()
    plt.style.use('ggplot')
    
    summary = """
    If you bought one stock of [%s] every week from %s to %s\n
    Total Investment: $%.2f
    Portfolio Value : $%.2f
    Profit / Loss   : $%.2f
    Profit Percent  : %.2f
    Average Cost    : %.2f
    Current Price   : %.2f
    Current Holding : %d
    """ % (ticker, startDate, endDate, cumulativeCost, currentPortfolioValue, currentPortfolioValue-cumulativeCost, profitPercentage, averageCost, currentPrice, currentHolding)

    # # print(summary)
    plt.text(0, 0.6 * y_max, summary, size=10)
    return plt, df, plt.figure(1)


def main():
    print("Hello World!")
    ticker = 'SPY'
    get_investment_returns_data('SPY')
    plt, df, fig = get_investment_returns_data(ticker)
    plt.savefig(ticker + ".png")
    plt.show()

if __name__ == "__main__":
    main()