import pandas as pd
from os import listdir
from os.path import isfile, join

dataPath = '/Users/lduque/Desktop/myProjects/moneyManager/loadData/data/quantopian/minuteIntraday/'

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

def getListOfAvailableStocks():
    """ Document asap
    """
    return [f.split('.')[0] for f in listdir(dataPath) if isfile(join(dataPath, f))]


timeSeriesCache = loadTimeSeriesCache()
def loadTimeSeries(stock, numSamples=None, endTime=None):
    """ Document asap
    """
    global timeSeriesCache
    df = timeSeriesCache[stock]
    df = df[(df.index<endTime)][-numSamples:].copy() if (numSamples!=None and endTime!=None) else df
    return df 



def countEmptyValuesInAvailableData():
    """ (probably not being used)
    """
    stocks = getListOfAvailableStocks()
    emptyInfo = []
    for s in stocks:
        df = loadTimeSeries(s)
        emptyCount = df.isna().sum()
        emptyInfo.append(emptyCount)
    dg = pd.concat(emptyInfo, axis=1)
    dg.columns=stocks
    return dg


def loadConsolidatedPrice(numSamples=None, endTime=None, stockList=None):
    """ Document asap
    """
    stockList = getListOfAvailableStocks() if stockList==None else stockList
    consolidatedTimeSeries = {S: loadTimeSeries(S, numSamples, endTime).consolidated for S in stockList}
    return consolidatedTimeSeries

def loadIncreaseTimeSeries(numSamples=None, endTime=None, stockList=None):
    """ Document asap
    """
    stockList = getListOfAvailableStocks() if stockList==None else stockList
    availablePrices = loadConsolidatedPrice(numSamples, endTime, stockList)
    return {S: (1+availablePrices[S].pct_change()).fillna(1) for S in availablePrices}


def getAvailableMarketMinutes():
    """ Document asap
    """
    return [s for s in timeSeriesCache['CSCO'].index]
