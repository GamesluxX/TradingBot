import abc
import Brokerage
import Parser
import time
import pandas as pd
import datetime
import os

class TradingSystem(abc.ABC):
    def __init__(self, api, stock_symbol):
        self.stock_symbol = stock_symbol
        self.api = api.api
        self.current_positions = []
        self.current_orders = []
        self.investment = 1000

    @abc.abstractmethod
    def place_sell_order(self):
        pass

    @abc.abstractmethod
    def place_buy_order(self):
        pass

    @abc.abstractmethod
    def trading_loop(self):
        pass

    def cancel_order(self, order_symbol):
        for order in self.current_orders:
            symbol = order.symbol
            id = order.id
            if order_symbol == symbol:
                self.api.cancel_order(id)
                print('Order cancelled: ' + order_symbol)

    def close_position(self, pos_symbol):
        for pos in self.current_positions:
            if pos.symbol == pos_symbol:
                print('Position closed: ' + pos_symbol + 'P/L: ' + str(pos.unrealized_plpc))

    def is_ordered(self, order_symbol):
        is_ordered = False
        for order in self.current_orders:
            if order.symbol == order_symbol:
                is_ordered = True
        return is_ordered

    def is_in_portfolio(self, stock_symbol):
        is_position = False
        for pos in self.current_positions:
            if stock_symbol == pos.symbol:
                is_position = True
        return is_position


class GermanStocks(TradingSystem):
    def __init__(self):
        super().__init__(Brokerage.AlpacaSocket(), 'DAX')
        self.data = pd.read_csv("src\dow_jones_stock_symbols.csv")
        self.trading_loop()
        self.parser = Parser.InvestComCSVParser()

    def place_buy_order(self, stock_symbol, qty):
        self.api.submit_order(
            symbol=stock_symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )

    def place_sell_order(self, stock_symbol, qty):
        self.api.submit_order(
            symbol=stock_symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
        )

    def trading_loop(self):
        count = 0
        while True:
            count += 1
            # run every second
            time.sleep(1)

            #store df in archive every 10sec
            if count > 9:
                count = 0

                #if directory is not yet created, create.
                if not os.path.exists("archive/" + str(datetime.date.today())):
                    os.makedirs("archive/" + str(datetime.date.today()))

                #safe current df with timestamp in respective directory
                self.stock_data.to_csv(path_or_buf="archive/" + str(datetime.date.today()) + "/" + datetime.datetime.now().strftime("%H_%M_%S") + ".csv")

            # refresh data
            #self.insider_trades_data = Parser.BoerseDeParser().refresh_data()
            self.stock_data = self.parser.refresh_data()

            self.current_orders = self.api.list_orders()
            self.current_positions = self.api.list_positions()

            for index, el in self.stock_data.iterrows():
                symbol = el['Symbol'].split('.')[0]

                #buy
                if el['5 Minutes'] == 'Strong Buy':
                    if not self.is_ordered(symbol) and not self.is_in_portfolio(symbol):
                        price = el['Last']

                        qty = round(self.investment / price, 0) - 1

                        self.place_buy_order(symbol, qty)

                        print('New order submitted: ' + str(qty) + ' x ' + symbol + " Price: " + str(price))

                #sell
                elif el['5 Minutes'] != 'Strong Buy':
                    if self.is_in_portfolio(symbol):
                        self.close_position(symbol)
                    elif self.is_ordered(symbol):
                        self.cancel_order(symbol)
GermanStocks()
