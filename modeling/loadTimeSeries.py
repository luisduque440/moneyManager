import pandas as pd
from os import listdir
from os.path import isfile, join

dataPath = '/Users/lduque/Desktop/myProjects/moneyManager/data/quantopian/minuteIntraday/'

def loadTimeSeries(stock, startDay, endDay):
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

def loadAvailablePriceTimeSeries(startDay, endDay):
    availableStocks = getListOfAvailableStocks()
    return {S: loadTimeSeries(S, startDay, endDay).consolidated for S in availableStocks}

def loadAvailableIncreaseTimeSeries(startDay, endDay):
    availablePrices = loadAvailablePriceTimeSeries(startDay, endDay)
    return {S: (1+availablePrices[S].pct_change()).fillna(1) for S in availablePrices}

def getListOfAvailableStocks():
    return [f.split('.')[0] for f in listdir(dataPath) if isfile(join(dataPath, f))]



