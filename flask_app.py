"""  HOW TO HOST PANDAS AND MATPLOTLIB ONLINE TEMPLATE"""

#Flask imports
from flask import Flask, render_template, send_file, make_response, url_for, Response
#Pandas and Matplotlib
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#other requirements
import io

#Data imports
from gendata import get_investment_returns_data


app = Flask(__name__)

#Pandas Page
@app.route('/')
@app.route('/pandas', methods=("POST", "GET"))
def GK():
    plt, df, fig = get_investment_returns_data('SPY')
    plt.savefig("static/chart.png")
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    return render_template('index.html',
                           PageTitle = "Pandas",
                           table=[df.to_html(classes='returns', index=False)], 
                           titles=df.columns.values)


# #Matplotlib page
# @app.route('/matplot', methods=("POST", "GET"))
# def mpl():
#     return render_template('matplot.html', PageTitle="Matplotlib")


# @app.route('/plot.png')
# def plot_png():
#     plt, df, fig = get_investment_returns_data('SPY')
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)