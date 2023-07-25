#!/usr/bin/env python
# coding: utf-8

# # Dash Application

# This application takes stock ticker as used in US stock market and return the timeseries chart of the stock closing price along with descriptive statistics for all of the parameters recorded.

# In[2]:


import yfinance as yf
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import dash_table
from dash.dependencies import Input, Output
from IPython.display import display
import warnings
warnings.filterwarnings("ignore")

# Create Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Stock Ticker Analysis"),
    html.Div([
        html.Label("Enter a stock ticker symbol:"),
        dcc.Input(
            id="input-ticker",
            type="text",
            value="AAPL"  # Default ticker symbol
        ),
    ]),
    html.Div([
        html.Label("Enter time series period (e.g., 1y, 3mo, 1d):"),
        dcc.Input(
            id="input-period",
            type="text",
            value="1y"  # Default time series period
        ),
    ]),
    html.Button("Submit", id="submit-button"),
    dcc.Graph(id="price-graph"),
    html.H3("Descriptive Statistics"),
    html.Div(id="statistics-output")
])

# Define callback for updating the graph and statistics
@app.callback(
    [Output("price-graph", "figure"), Output("statistics-output", "children")],
    [Input("submit-button", "n_clicks")],
    [dash.dependencies.State("input-ticker", "value"),
     dash.dependencies.State("input-period", "value")]
)
def update_output(n_clicks, ticker, period):
    if ticker:
        # Retrieve stock data from Yahoo Finance
        data = yf.download(ticker, period=period, progress=False)
        data.reset_index(inplace=True)
        # Create the price graph
        fig = {
            "data": [
                {"x": data['Date'], "y": data["Close"], "type": "line", "name": ticker}
            ],
            "layout": {
                "title": f"{ticker} Price Time Series"
            }
        }
        # Calculate descriptive statistics and round to 2 decimal places
        statistics = data.describe().transpose().reset_index()
        statistics = statistics.round(2)
        # Create the statistics table
        statistics_table = dash_table.DataTable(
            data=statistics.to_dict("records"),
            columns=[{"name": c, "id": c} for c in statistics.columns],
            style_as_list_view=True,
            style_cell={"padding": "5px"},
            style_header={"fontWeight": "bold"}
        )
        return fig, statistics_table
    else:
        return {}, ""

# Run the app
if __name__ == "__main__":
    app.run_server(mode="inline", port=8054)

