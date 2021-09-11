import os
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta, WE
from math import log10, floor

valid_tickers = [ "UVXY", "VXX", "ARKG", "ITB", "IEFA", "INDA", "VIXY", "RSX", "IGV", "GOVT", "SVXY", "EZU", "VLUE", "USMV", "REM", "USHY", "EFV", "PAVE", "QUAL", "JPST", "BBJP", "MTUM", "ARKQ", "CBOE", "JMST", "BBEU", "HYD", "ICSH", "ARKX", "IGE", "BBAX", "ITA", "ECH", "EFG", "NULV", "IEO", "IYT", "VUSB", "BBCA", "VNM", "FLOT", "EFAV", "IDV", "RYLD", "ESGV", "PJUL", "NOBL", "HEFA", "ITM", "MOAT", "PICK", "TAIL", "NEAR", "ICVT", "ACWV", "VSGX", "ACIO", "CNYA", "VIXM", "ESML", "SLVP", "BUFR", "COWZ", "EEMV", "SMIN", "IFRA", "ICF", "FGRO", "BUFD", "OMFL", "IYZ", "IAGG", "FMIL", "DWLD", "PRNT", "NUSC", "SMB", "PTLC", "IZRL", "IGHG", "FCTR", "EPRF", "CEMB", "SMDV", "FPRO", "EMHY", "CALF", "EMGF", "OGIG", "BBUS", "IBML", "PSMM", "FBCG", "VCEB", "KNG", "PAWZ", "SVAL", "XMPT", "ESG", "QMOM", "EGIS", "FPFD", "BMAY", "SECT", "IGEB", "MBCC", "SYLD", "PSEP", "IEFN", "PDEC", "MLN", "PTMC", "EOPS", "BDEC", "BBIN", "VXZ", "VOTE", "FFEB", "SMMV", "OILK", "NURE", "EDEN", "NJAN", "EWUS", "QTAP", "IYJ", "JEMA", "BBRE", "TMFC", "NUMV", "GOVZ", "MFMS", "IYLD", "OUSA", "FBCV", "CEFS", "VFVA", "GVI", "PJAN", "REGL", "ADME", "SHYD", "MSVX", "FLQL", "SMMD", "LYFE", "PTNQ", "FSMO", "GOAT", "AUGZ", "BALT", "FAUG", "IEIH", "MSTB", "GTIP", "BAUG", "GSST", "DSEP", "HEGD", "IQDG", "VFQY", "FRDM", "USEP", "ENOR", "PSMC", "HEEM", "NUMG", "ZECP", "SHAG", "UAUG", "NULG", "BSEP", "XSHD", "BFEB", "FCPI", "LUXE", "TMDV", "BBSA", "PAUG", "MPRO", "IBMQ", "XVV", "FLDR", "LQDI", "IEHS", "DDLS", "DRSK", "PBTP", "DIVB", "PAPR", "THY", "VAMO", "LVHI", "WFHY", "NUEM", "VFMV", "DFNV", "HYDB", "GAA", "DFEB", "FJAN", "JCPB", "HELX", "IMOM", "JPIB", "GSEW", "NULC", "TOKE", "OEUR", "RSXJ", "XTJL", "FFHG", "EWGS", "IBMM", "BGLD", "MEAR", "CSM", "IVAL", "LKOR", "FYLD", "TTAI", "MRSK", "WUGI", "DINT", "IETC", "IVRA", "BOSS", "NUDM", "TDV", "XSHQ", "CBTG", "TILT", "DAPR", "TTAC", "ISVL", "BJAN", "BJUN", "PBSM", "QPFF", "GSUS", "IVSG", "VFMO", "IBHC", "JPHY", "GVAL", "PSFF", "POCT", "GHYG", "FIBR", "FDEC", "QVAL", "HSRT", "DFNL", "DAUG", "BUFF", "FDG", "IBMN", "UMAY", "ADFI", "FFSG", "MAMB", "QCON", "TBJL", "EUCG", "TMAT", "IVDG", "HYHG", "NAPR", "DALT", "IEME", "PTEU", "JULZ", "PMAY", "UNOV", "JMUB", "EFNL", "NOCT", "FMAG", "WFIG", "DUDE", "FFTI", "EMDV", "ALTS", "AESR", "FOMO", "OMFS", "STOT", "IDME", "PSMB", "DUSA", "EFAD", "EMSH", "UJUL", "DDEC", "XDQQ", "IDHD", "IBHA", "EYLD", "XJH", "MDEV", "IECS", "HYMU", "IVLC", "ARCM", "ESGG", "XBAP", "DJUL", "KJAN", "DFND", "AVDR", "FLV", "VWID", "WDNA", "IBHB", "DJUN", "ALFA", "UFEB", "FDEM", "VFMF", "IEDI", "FAPR", "FLQM", "IBMP", "IBHD", "PBEE", "DFHY", "IQM", "DDWM", "SFHY", "FDEV", "IBHE", "KWT", "FLIA", "GLDB", "IGLD", "KNGS", "SLT", "EURZ", "FLBL", "IMFL", "TAEQ", "UOCT", "IAUF", "NJUL", "HYXU", "AFIF", "FLQS", "FLHY", "PBUS", "FFTG", "FJUL", "OUSM", "QJUN", "BOB", "BUYZ", "IBMO", "BAPR", "PBND", "AMER", "EAOA", "YPS", "QLC", "PJUN", "WLDR", "DECZ", "TSOC", "GCOW", "FEDX", "DBJA", "HCRB", "USMF", "ATMP", "EMTL", "XJR", "PMAR", "TFIV", "MAGA", "VFLQ", "VMOT", "FMAY", "RESE", "ACSI", "EUDV", "FAIL", "PSMG", "MINN", "PNOV", "GMOM", "SFIG", "SULR", "APRZ", "DURA", "DBOC", "MAYZ", "OSCV", "PFEB", "AGT", "DEFN", "ICOW", "BOCT", "FNOV", "KJUL", "MOTI", "STLG", "DOCT", "FJUN", "FOCT", "PLRG", "QMAR", "AVDG", "BLDG", "DMAR", "HEET", "MRGR", "TRTY", "VIRS", "XDAT", "BJUL", "BMAR", "BNOV", "CFCV", "DJAN", "DMAY", "DNOV", "DSJA", "DSOC", "EAOK", "EAOM", "EAOR", "ESCR", "ESEB", "ESHY", "FEBZ", "FMAR", "FSEP", "FUNL", "FUT", "GSEE", "GSID", "HYIN", "IBHF", "IBHG", "IGRO", "IMLP", "JANZ", "JUNZ", "KAPR", "KOCT", "LEAD", "LIV", "LSLT", "MAAX", "MARZ", "MBBB", "MBND", "MIG", "NOVZ", "OCTZ", "PBDM", "PEX", "PLTL", "PSCJ", "PSCW", "PSCX", "PSFD", "PSFJ", "PSFM", "PSMD", "PSMJ", "PSMR", "PWS", "PXUS", "QDEC", "QTJL", "RDFI", "REC", "RESD", "RODE", "RODI", "ROMO", "RTAI", "SEPZ", "SPMV", "STLV", "TCTL", "TEGS", "TFJL", "TFLT", "TSJA", "UAPR", "UDEC", "UJAN", "UJUN", "UMAR", "USEQ", "WIL", "XBJL", "XDAP", "XDJL", "XDSQ", "XJUN", "XTAP", "YDEC", "YJUN", "YMAR"]

def is_valid_ticker(t):
    return t in valid_tickers

duration=10 #years

def check_valid_tickers(ticker):
    tickers = ticker.split()
    error_msg = "Invalid ticker: "
    error_count = 0
    valid_tickers = []
    for t in tickers:
        t = t.strip()
        if is_valid_ticker(t):
            valid_tickers += t
        elif yf.Ticker(t).info['regularMarketPrice'] == None:
                error_msg = error_msg + t + " "
                error_count += 1

    if error_count > 0:
        error_msg = error_msg + ". Results returned for: "
        if valid_tickers.__len__() > 0:
            error_msg += " ".join(valid_tickers)
            ticker = " ".join(valid_tickers)
        else:
            ticker = "SPY QQQ IWM"
    return ticker, error_count > 0, error_msg

def format_func(value, tick_number=None):
    num_thousands = 0 if abs(value) < 1000 else floor (log10(abs(value))/3)
    value = round(value / 1000**num_thousands, 2)
    return f'{value:g}'+' KMGTPEZY'[num_thousands]

def get_investment_returns_data(ticker, investment_amt_per_week):
    cashInHand=0
    InvestmentAmt=investment_amt_per_week
    startDate = datetime.now() - relativedelta(years=duration)
    startDate = startDate.strftime("%Y-%m-%d")
    endDate = datetime.now().strftime("%Y-%m-%d")
    data = yf.download(ticker,startDate, endDate, interval = "1wk")
    strDate = ""
    currentHolding = 0
    cumulativeCost = 0.0
    currentPortfolioValue = 0.0
    averageCost = 0.0
    currentPrice = 0.0
    # print(data)
    mutiticker = ticker.split().__len__() > 1
    # print("Date", "CurrentHolding", "CurrentPrice", "AveragePrice", "CumulativeCost", "CurrentPortfolioValue", "Profit/Loss")
    portfolioData = []
    for i, row in data.iterrows():
        isnan = math.isnan(row['Open'][0]) if mutiticker else math.isnan(row['Open'])
        if isnan == False:
            datetime_object = i.to_pydatetime()
            strDate = datetime_object.strftime("%Y-%m-%d")
            datetime_object = i.to_pydatetime()
            strDate = datetime_object.strftime("%Y-%m-%d")
            #sum(row['Open'][0]) if multiticker gives the sum of price for all tickers
            currentPrice = round(float(sum(row['Open'])), 2) if mutiticker else round(float(row['Open']), 2)
            cashInHand=cashInHand+InvestmentAmt
            totalUnitsToBuy=int(cashInHand/currentPrice)
            currentHolding += totalUnitsToBuy
            totalInvestmentThisCycle=totalUnitsToBuy*currentPrice
            cumulativeCost = round(cumulativeCost + totalInvestmentThisCycle, 2)
            cashInHand=cashInHand-totalInvestmentThisCycle
            currentPortfolioValue = round(currentHolding * currentPrice, 2) + cashInHand
            averageCost = round(cumulativeCost/currentHolding, 2)
            mytuple = (strDate, currentHolding, currentPrice, averageCost, cumulativeCost, currentPortfolioValue, currentPortfolioValue-cumulativeCost,cashInHand)
            portfolioData.append(mytuple)
            # print(mytuple)

    profitPercentage = (currentPortfolioValue-cumulativeCost)/cumulativeCost*100
    df = pd.DataFrame(portfolioData, columns=["Date", "CurrentHolding", "CurrentPrice", "AveragePrice", "CumulativeCost", "CurrentPortfolioValue", "Profit/Loss", "CashInHand"])
    df.round(2)
    x = df['Date']
    plt.rcParams["figure.figsize"] = (10,6)
    plt.rcParams['font.family'] = 'monospace'
    fig, ax = plt.subplots()
    plt.plot(x, df['CumulativeCost'], label='CumulativeCost')
    plt.plot(x, df['CurrentPortfolioValue'], label='CurrentPortfolioValue')
    plt.ylabel('Portfolio Value $$$')
    plt.xlabel('Investment Dates')
    y_min, y_max = plt.ylim()
    plt.ticklabel_format(axis='y', style='', useOffset=False)

    plt.title('Weekly Investment - 10 Year Returns')
    plt.legend(loc="lower right")
    plt.xticks(x[::20],  rotation='vertical')
    plt.tight_layout()
    plt.style.use('ggplot')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    
    
    # summary = """
    # If you bought one stock of [%s] every week from %s to %s\n
    summary = """
    If you invested $%d 
    To buy [%s] every week from %s to %s
    Your portfolio value would be as follows:
    Portfolio Value : $%.2f
    Total Investment: $%.2f
    Profit / Loss   : $%.2f
    Profit Percent  : %.2f
    Average Cost    : %.2f
    Current Price   : %.2f
    Current Holding : %d
    Cash In Hand    : %.2f
    """ % (InvestmentAmt, ticker, startDate, endDate, currentPortfolioValue, cumulativeCost, currentPortfolioValue-cumulativeCost, profitPercentage, averageCost, currentPrice, currentHolding,cashInHand)

    plt.text(0, 0.5 * y_max, summary, size=10)
    if os.name == 'nt':
        plt.savefig("static/chart.png")
    else:
        plt.savefig("/home/richboy/richboy/static/chart.png")
    return plt, df

def main():
    print("Hello World!")
    ticker = 'SPY QQQ'
    plt, df = get_investment_returns_data(ticker, 10000)
    # plt.savefig(ticker + ".png")
    plt.show()

if __name__ == "__main__":
    main()