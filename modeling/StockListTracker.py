
import os, time
import pandas as pd
from datetime import datetime, timedelta
from .stockModel import stockModel



class StockListTracker():
    """ This is the first strategy to deploy
    """
    def __init__(self, tradingDay=None, stockList=None, tradingTimeZone="America/New_York"):
        os.environ["TZ"] = tradingTimeZone
        self.tradingTimeZone = tradingTimeZone
        self.tradingDay = datetime.now().replace(hour=0, minute =0, second=0, microsecond=0) if tradingDay==None else tradingDay
        self.stockList = self._getDowJonesSymbols() if stockList==None else stockList
        self.stockModelDictionary = getStockModelDictionary(self.stockList)


    def _getDowJonesSymbols(self):
        return ['GOOGL', 'IBM', 'UNIMPLEMENTED']


    def getStockModelDictionary(self, numTrainingDays=28):
        """ Trains all the stockModels
        """
        startTrainTime = (self.tradingDay - timedelta(days=numTrainingDays))
        endTrainTime = self.tradingDay
        modelDictionary = {}
        for symbol in stockSymbols:
            modelDictionary[symbol] = stockModel(symbol, startTrainTime, endTrainTime).fullyTrain()
        return modelDictionary

    def getLastTradeableMinute(self)
        print("method getLastTradeableMinute() is not available yet")
        return datetime(1970,1,1)


    def getLatestOrderSuggestions(self):
        """ returns a dictionary with the orders that our stockModels suggest

        """
        lastTradeableMinute = self.getLastTradeableMinute()
        # iterates on all the models to produce a list/dictionary with orders (probably a list)
        df = pd.DataFrame()
        return df


    def getExecutableOrders():
        """ From the infor
        """
        orderSuggestions = self.getLatestOrderSuggestions()
        ## ... filters 
        orders = {}
        return orders
