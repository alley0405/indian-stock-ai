from abc import ABC, abstractmethod

class BrokerBase(ABC):

    @abstractmethod
    def buy(self, symbol, quantity):
        pass

    @abstractmethod
    def sell(self, symbol, quantity):
        pass

    @abstractmethod
    def get_ltp(self, symbol):
        pass
