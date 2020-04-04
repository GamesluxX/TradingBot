import alpaca_trade_api as tradeapi
from alpha_vantage.timeseries import TimeSeries
import pandas as pd


class AlpacaSocket():
    def __init__(self):
        self.api = tradeapi.REST('PKJ7X20KA4SACL4D1KQD', 'chXfEjsnaB5Q0WVoVFeUE78g7AXZfF9OW/ODQP6j',
                                 'https://paper-api.alpaca.markets',
                                 api_version='v2')  # or use ENV Vars shown below
        self.account = self.api.get_account()
        self.brokerage_data = None

    def refresh_data(self):
        self.brokerage_data = self.api.get_barset(['SAP'], 'minute', 1000).df


class AlphaVantage():
    def __init__(self, stock_symbol):
        # Your key here
        self.key = 'PG5HZA063CKOYVHF'
        self.ts = TimeSeries(self.key)
        self.stock_data = None
        self.stock_data, meta = self.ts.get_intraday(symbol=stock_symbol,interval='1min',outputsize='compact')
        print(self.stock_data)

