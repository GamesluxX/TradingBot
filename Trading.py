import abc
import Brokerage


class TradingSystem(abc.ABC):
    def __init__(self, api, stock_symbol):
        self.stock_symbol = stock_symbol
        self.api = api(self.stock_symbol)

    @abc.abstractmethod
    def place_sell_order(self):
        pass

    @abc.abstractmethod
    def place_buy_order(self):
        pass

    @abc.abstractmethod
    def trading_loop(self):
        pass


class DAX(TradingSystem):
    def __init__(self):
        super().__init__(Brokerage.AlpacaSocket(), 'DAX')

    def place_buy_order(self):
        pass

    def place_sell_order(self):
        pass

    def trading_loop(self):
        pass
