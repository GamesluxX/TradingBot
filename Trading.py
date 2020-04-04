import abc
import Brokerage
import Parser
import time
import pandas as pd

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
        try:
            self.api.close_position(pos_symbol)
            print('Position closed: ' + pos_symbol)
        except:
            pass

    def is_ordered(self, order_symbol):
        is_ordered = False
        for order in self.current_orders:
            if order.symbol == order_symbol:
                is_ordered = True
        return is_ordered


class GermanStocks(TradingSystem):
    def __init__(self):
        super().__init__(Brokerage.AlpacaSocket(), 'DAX')
        self.data = pd.read_csv("src\dow_jones_stock_symbols.csv")
        self.trading_loop()

    def place_buy_order(self, order_symbol, qty):
        self.api.submit_order(
            symbol=order_symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )

    def place_sell_order(self, symbol, qty):
        self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
        )

    def trading_loop(self):

        while True:
            # run every second
            time.sleep(1)

            # refresh data
            self.insider_trades_data = Parser.BoerseDeParser().refresh_data()
            self.stock_data = Parser.InvestComCSVParser().refresh_data()

            print(self.api.list_orders())

            self.current_orders = self.api.list_orders()
            self.current_positions = self.api.list_positions()

            # buy
            for index, el in self.stock_data.iterrows():
                symbol = el['Symbol'].split('.')[0]
                if el['5 Minutes'] == 'Strong Buy':
                    if not self.is_ordered(symbol):
                        price = el['Last']

                        qty = round(self.investment / price, 0) - 1

                        self.place_buy_order(symbol, qty)

                        print('New order submitted: ' + str(qty) + ' x ' + symbol + " Price: " + str(price))

            # sell
            for index, el in self.stock_data.iterrows():
                if el['5 Minutes'] != 'Strong Buy':
                    if symbol in self.current_positions:
                        self.close_position(symbol)
                    elif symbol in self.current_orders:
                        self.cancel_order(symbol)


GermanStocks()
