import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime

dataPath = '/Users/lduque/Desktop/myProjects/moneyManager/loadData/data/quantopian/minuteIntraday/'


def loadTimeSeries(stock, startDay, endDay):
    """ this should be better called loadCandleData(?)
    """
    filename = stock+'.csv'
    df = pd.read_csv(dataPath+filename).drop(columns=['symbol'])
    df['date']= pd.to_datetime(df.date, infer_datetime_format=True) 
    df = df[(df.date>=startDay) & (df.date<endDay)].copy()
    df = df.set_index('date')
    df.columns = ['open','high','low','close','volume']
    # (the following does not belong here !!!!!!)
    df['consolidated']=df.drop(columns='volume').mean(axis=1) 
    return df

def loadPriceTimeSeries(startDay, endDay, stockList=None):
    stockList = getListOfAvailableStocks() if stockList==None else stockList
    fullTimeSeries = {S: loadTimeSeries(S, startDay, endDay).consolidated for S in stockList}
    return fullTimeSeries

def loadIncreaseTimeSeries(startDay, endDay, stockList=None):
    stockList = getListOfAvailableStocks() if stockList==None else stockList
    availablePrices = loadPriceTimeSeries(startDay, endDay, stockList)
    return {S: (1+availablePrices[S].pct_change()).fillna(1) for S in availablePrices}

def getListOfAvailableStocks():
    return [f.split('.')[0] for f in listdir(dataPath) if isfile(join(dataPath, f))]



