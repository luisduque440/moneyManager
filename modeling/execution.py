# Notes
# * Need a wrapper of pipeline type objects that makes its evaluation easier.
# * Maybe each pipeline can generate its own model? lets call it a stockPipeline
# * The pipelines/stock model must be designed to 'easily' support expansions, specially we have to be able to easily feed it with exogenous data


import os, time
import pandas as pd
from datetime import datetime, timedelta


class stockModel():
    """Wrapper of a single stock-pipeline with its respective thresholds, train datasets and evaluators
    """
    def __init__(self, stockSymbol, startDay, endDay):
        self.stockSymbol = stockSymbol
        self.startDay = startDay
        self.endDay = endDay
        self.validModel = None
        self.pipelineInfo = {}
        self.percentageOfDataSetAvailable = None
    
    def fullyTrain(self):
        self.gatherData()
        return self

    def gatherData(self):
        df = pd.DataFrame()
        return df

    
def getStockModelDictionary(stockSymbols, startDay=None, endDay=None):
    """ Trains all the stockModels
    """
    modelDictionary = {}
    for symbol in stockSymbols:
        modelDictionary[symbol] = stockModel(symbol, startDay, endDay).fullyTrain()
    return modelDictionary


def getCurrentMinute(timezone=None):
    cMinute = datetime.now()
    cMinute.replace(second=0, microsecond=0)
    return cMinute

def getLastAvailableMinute(timezone=None):
    print("method getLastAvailableMinute() is not available yet")
    return datetime(1970,1,1)

def getTodayCloseTime(timezone=None):
    return datetime.now().replace(hour=16, minute =0, second=0, microsecond=0)

def getTodayOpenTime(timezone=None):
    return datetime.now().replace(hour=9, minute =0, second=0, microsecond=0)

def marketIsOpen():
    cTime = datetime.now()
    openTime = getTodayOpenTime()
    closeTime = getTodayCloseTime()
    return (cTime>=openTime and cTime<closeTime())

def marketClosedToday():
    cTime = datetime.now()
    closeTime = getTodayCloseTime()
    return cTime>=closeTime


def getOrderSuggestions(stockModelDictionary, minute):
    """ returns a dictionary with the orders that our stockModels suggest
    """
    df = pd.DataFrame()
    return df


def getExecutableOrders():
    """ From the infor
    """
    orders = {}
    return orders
    
    
def executeOrders(orders):
    """ Execute a dictionary with orders
    """
    
    return 

def produceDailyReport():
    """ produces a detailed report of what happened during the day
    """
    pass
    return "Daily Report"


#executes a couple of hours before markets open
stockList = ['GOOGL', 'IBM']

def dailyTradingRoutine():
	os.environ["TZ"] = "America/New_York"
    stockModelDictionary = getStockModelDictionary(stockList) 
    lastTradedMinute = datetime.now().replace(hour=0, minute =0, second=0, microsecond=0)

    while(not marketClosedToday()):
        lastAvailableMinute = getLastAvailableMinute()
        if lastAvailableMinute>lastTradedMinute:
            orderSuggestions = getOrderSuggestions(stockModelDictionary, lastAvailableMinute)
            orders = getExecutableOrders(orderSuggestions)
            executeOrders(orders)
            lastTradedMinute = lastAvailableMinute
        break

    produceDailyReport()
    print("--- end of daily trading routine ---")
