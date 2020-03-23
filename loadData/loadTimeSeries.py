import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime

dataPath = '/Users/lduque/Desktop/myProjects/moneyManager/loadData/data/quantopian/minuteIntraday/'
timeSeriesCache = loadTimeSeriesCache()

def loadTimeSeriesCache():
    """ Document asap
    """
    stockList = getListOfAvailableStocks()
    timeSeriesCache = {}
    for stock in stockList: 
        filename = stock+'.csv'
        df = pd.read_csv(dataPath+filename).drop(columns=['symbol'])
        df['date']= pd.to_datetime(df.date, infer_datetime_format=True) 
        df = df.set_index('date')
        df.columns = ['open','high','low','close','volume']    
        df['consolidated']=df.drop(columns='volume').mean(axis=1) 
        timeSeriesCache[stock]=df.copy()
    return timeSeriesCache

def loadTimeSeries(stock, startTime, endTime):
    """ Document asap
    """
    global timeSeriesCache
    df = timeSeriesCache[stock]
    df = df[(df.date>=startTime) & (df.date<endTime)].copy()
    return df

def loadConsolidatedPrice(startTime, endTime, stockList=None):
    """ Document asap
    """
    stockList = getListOfAvailableStocks() if stockList==None else stockList
    consolidatedTimeSeries = {S: loadTimeSeries(S, startTime, endTime).consolidated for S in stockList}
    return consolidatedTimeSeries

def loadIncreaseTimeSeries(startTime, endTime, stockList=None):
    """ Document asap
    """
    stockList = getListOfAvailableStocks() if stockList==None else stockList
    availablePrices = loadConsolidatedPrice(startTime, endTime, stockList)
    return {S: (1+availablePrices[S].pct_change()).fillna(1) for S in availablePrices}

def getListOfAvailableStocks():
    """ Document asap
    """
    return [f.split('.')[0] for f in listdir(dataPath) if isfile(join(dataPath, f))]
