import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime

dataPath = '/Users/lduque/Desktop/myProjects/moneyManager/data/quantopian/minuteIntraday/'
startDay = datetime(2019,1,1)
endDay = datetime(2020,1,1)


def loadTimeSeries(stock, startDay=startDay, endDay=endDay):
    """ 
    """
    filename = stock+'.csv'
    df = pd.read_csv(dataPath+filename).drop(columns=['symbol'])
    df['date']= pd.to_datetime(df.date, infer_datetime_format=True) 
    df = df[(df.date>=startDay) & (df.date<endDay)].copy()
    df = df.set_index('date')
    df.columns = ['open','high','low','close','volume']
    df['consolidated']=df.drop(columns='volume').mean(axis=1)
    return df

def loadPriceTimeSeries(startDay=startDay, endDay=endDay, stockList=None):
    stockList = getListOfAvailableStocks() if stockList==None else stockList
    fullTimeSeries = {S: loadTimeSeries(S, startDay, endDay).consolidated for S in stockList}
    return fullTimeSeries

def loadIncreaseTimeSeries(startDay=startDay, endDay=endDay, stockList=None):
    stockList = getListOfAvailableStocks() if stockList==None else stockList
    availablePrices = loadPriceTimeSeries(startDay, endDay, stockList)
    return {S: (1+availablePrices[S].pct_change()).fillna(1) for S in availablePrices}

def getListOfAvailableStocks():
    return [f.split('.')[0] for f in listdir(dataPath) if isfile(join(dataPath, f))]



