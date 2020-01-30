# printing time series on quantopian
from datetime import datetime
import pandas as pd
import numpy as np
import sklearn as sk
import scipy as sp
from datetime import datetime
import pandas as pd

def loadTimeSeries(symbol, startDay, endDay):
    fields = ['price', 'open_price', 'high', 'low', 'close_price', 'volume']
    L = [get_pricing([symbol], start_date=startDay, end_date=endDay, fields=field, frequency='minute') for field in fields]
    df = pd.concat(L, join='inner', axis=1)
    df.columns=fields
    return df

def nicePrintDf(df):
    dates = df.index
    rows = df.values
    printList(['date']+list(df.columns))
    for i in range(len(df)):
        printList([dates[i].strftime('%Y-%m-%d %H:%M')]+list(rows[i]))
        
def printList(A):
    L = ''
    for s in A[:-1]:
        L+=str(s)+','
    print(L+str(A[-1]))
    
    
startDay = datetime(2019,1,1)
endDay = datetime(2020,1, 1)

symbol = 'IBM'
dg=loadTimeSeries(symbol=symbol, startDay=startDay, endDay=endDay)
dg = dg.fillna('')
nicePrintDf(dg)
