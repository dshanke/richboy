"""  HOW TO HOST PANDAS AND MATPLOTLIB ONLINE TEMPLATE"""

#Flask imports
from flask import Flask, render_template, send_file, make_response, url_for, Response, request
#Pandas and Matplotlib
import pandas as pd
import time, os

#other requirements
import io

#Data imports
from gendata import get_investment_returns_data, check_valid_tickers


app = Flask(__name__)

#Pandas Page
@app.route('/', methods=("POST", "GET"))
#@app.route('/pandas', methods=("POST", "GET"))
def get_returns():
    ticker_name = "SPY QQQ IWM"
    error_msg = ""
    if request.method == "POST":
        ticker_name = request.form.get("ticker_name")
    try:
        plt, df = get_investment_returns_data(ticker_name)
    except:
        error_msg = "Please provide valid tickers. Your query has not been processed"
        ticker_name = "SPY QQQ IWM"
        plt, df = get_investment_returns_data(ticker_name)
    return render_template('index.html',
                           PageTitle = "10YearReturns",
                           chart_file="static/chart.png",
                           error_message=error_msg,
                           ticker_name=ticker_name,
                           table=[df.to_html(classes='ws_data_table', index=False)], 
                           titles=df.columns.values)


if __name__ == '__main__':
    app.run(debug=True)