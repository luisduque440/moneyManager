import pandas as pd
import numpy as np
from sys import platform

def loadTimeSeries(stock, startDay, endDay):
    """ This function depends on the platform!!!
    """
    if platform=='darwin':
        names = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        filename = stock+'_adjusted.txt'
        df = pd.read_csv('data/sampleKibotData/minuteIntraday_modified/'+filename, header=None, names=names)
        df['DateTime']= pd.to_datetime((df.Date+' '+df.Time), infer_datetime_format=True) 
        df = df.drop(columns=['Date', 'Time'])
        df = df.set_index('DateTime')
    else:
        # https://www.quantopian.com/posts/minute-bar-data-in-research
        print('not implemented yet')
    return df[['Open', 'High', 'Low', 'Close', 'Volume']] # (!!!!)this could change


def createTrainingDataSet(stock1, stock2, startDate, endDate, pastStart=4, futureEnd=-2):
    """ Start documenting now.
        This requires more defensive code: look for instance at the old implementation of this function.
    """
    ds1 = loadTimeSeries(stock1, startDate, endDate)
    df1 = pivotWindow(ds1, pastStart, -1) 
    s = ds1[['Open','High','Low','Close']].apply(np.mean, axis=1)
    df1['increase'] = (s.shift(-futureEnd)-s.shift(-1))

    ds2 = loadTimeSeries(stock2, startDate, endDate)
    df2 = pivotWindow(ds2, pastStart, -1) 
    s = ds2[['Open','High','Low','Close']].apply(np.mean, axis=1)
    df2['increase'] = (s.shift(-futureEnd)-s.shift(-1))

    df1.columns = [stock1+col for col in df1.columns]
    df2.columns = [stock2+col for col in df2.columns]
    dg = df1.merge(df2, how='inner', left_index=True, right_index=True)
    dg['target']= dg[stock1+'increase'] > dg[stock2+'increase']
    dg = dg.drop(columns=[stock1+'increase', stock2+'increase'])
    return dg
    



def pivotWindow(ds, start, end, columns = ['Open', 'High', 'Low', 'Close', 'Volume']):
    """ start documenting this 
    """
    ds['DateTime']=list(ds.index)
    pivotedCols = [pivotSeries(ds['DateTime'], start, end) ]+[pivotSeries(ds[col], start, end) for col in columns]
    dg = pd.concat(pivotedCols, axis=1)
    dg.columns = ['DateTime'] + columns
    dg['validRow'] = (ds.DateTime.shift(end+1)-ds.DateTime.shift(start)).apply(lambda x: (start-end-1)==x.seconds/60)
    return dg

def pivotSeries(s, start, end): 
    """ start documenting this 
    """
    return pd.concat([s.shift(i) for i in range(start, end, -1)], axis=1).apply(lambda x: list(x), axis=1)


