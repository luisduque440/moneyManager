
import pandas as pd
from datetime import datetime, timedelta
from .stockModel import stockModel


class StockListTracker():
    """ This is the first strategy to deploy
    """
    def __init__(self):
        """ DONE
        """
        self.tradingDay = datetime.now().replace(hour=0, minute =0, second=0, microsecond=0)
        self.stockSymbols = self._getDowJonesSymbols()
        self.stockModelDictionary = getStockModelDictionary(self.stockList)


    def getStockModelDictionary(self, numTrainingDays=28):
        """ DONE. Trains all the stockModels
        """
        startTrainTime = (self.tradingDay - timedelta(days=numTrainingDays))
        endTrainTime = self.tradingDay
        modelDictionary = {}
        for symbol in self.stockSymbols:
            modelDictionary[symbol] = stockModel(symbol, startTrainTime, endTrainTime).fullyTrain()
        return modelDictionary

    def modelsCanRunAtCurrentMinute(self, currentMinute):
        """ UNFINISHED. Plataform dependent
        """
        return


    def getLatestOrderSuggestions(self):
        """ DONE. returns a dictionary with the orders that our stockModels suggest
        """
            return {stock: self.modelDictionary[stock].getLatestOrderSuggestions() for stock in self.stockList}


    def getExecutableOrders():
        """ Main strategy: puts together the information coming from all the models
            We want to buy/sell an stock if:
                (1) We have too little/too much of it compared to the proportions of Dow Jones.
                (2) We have not trade that stock on a certain period of time.
                (3) Our models suggest that we should buy it/ sell it.
        """
        orderSuggestions = self.getLatestOrderSuggestions()
        dowJonesProportions = self.getDowJonesProportions()
        portFolioProportions = self.getPorfolioProportions()
        latestTransactionTimes = self.getLatestTransactionTimes()

        # implement the actual strategy, report the times in which the orders must be executed.

        orders = {}
        return orders

    def getDowJonesProportions(self):
        """ Returns a dictionary of percentages (adds up to 1) of how money is allocated in the DowJones
        """
        dowJonesProportions={} 
        return dowJonesProportions

    def getPorfolioProportions(self):
        """ Returns a dictionary of percentages (adds up to 1) of how money is allocated in our portfolio
        """
        dowJonesProportions={self} 
        return dowJonesProportions

    def getLatestTransactionTimes(self):
        """ Returns a dictionary of percentages (adds up to 1) of how money is allocated in our portfolio
        """
        return 


    def _getDowJonesSymbols(self):
        """ Done, note: IOH is not part of Dow, but I already have some familiarity with the pair (IBM, IOH)
        """
        dowJonesSymbols =  [
            "MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DOW", "XOM", "GS", "HD", "IBM", "INTC", 
            "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ", "V", "WBA", "WMT", "IOH"
        ]
        return dowJonesSymbols

