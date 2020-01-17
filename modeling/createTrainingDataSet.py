import pandas as pd
import numpy as np
from datetime import datetime
from sys import platform

def loadTimeSeries(stock, startDay, endDay):
	""" 
	"""
	filename = stock+'.csv'
	df = pd.read_csv('data/quantopian/minuteIntraday/'+filename).drop(columns=['symbol'])
	df['date']= pd.to_datetime(df.date, infer_datetime_format=True) 
	df = df[(df.date>=startDay) & (df.date<endDay)].copy()
	df = df.set_index('date')
	return df


def createTrainingDataSet(stock1, stock2, startDay, endDay, pastStart=4):
    """ Start documenting now.
        This requires more defensive code: look for instance at the old implementation of this function.
    """
    ds1 = loadTimeSeries(stock1, startDay, endDay)
    s = ds1.drop(columns='volume').apply(np.mean, axis=1)
    ds1['FutureIncrease'] = (s.pct_change().shift(-2)+1)

    ds2 = loadTimeSeries(stock2, startDay, endDay)
    s = ds2.drop(columns='volume').apply(np.mean, axis=1)
    ds2['FutureIncrease'] = (s.pct_change().shift(-2)+1)

    ds1.columns = ['stock1'+col for col in ds1.columns]
    ds2.columns = ['stock2'+col for col in ds2.columns]
    dg = ds1.merge(ds2, how='inner', left_index=True, right_index=True)
    dg['target']= dg.stock1FutureIncrease > dg.stock2FutureIncrease 
    dg = dg.drop(columns=['stock1FutureIncrease', 'stock2FutureIncrease'])

    columnsToPivot = list(dg.columns)
    columnsToPivot.remove('target')
    df = pivotWindow(dg, pastStart, -1, columnsToPivot)
    return df


def pivotWindow(ds, start, end, columnsToPivot):
    """ we could add defensive code here, but wont for now 
    """
    columnsNotToPivot = [col for col in ds.columns if col not in columnsToPivot]
    pivotedCols = [pivotSeries(ds[col], start, end) for col in columnsToPivot]
    notPivotedCols = [ds[col] for col in columnsNotToPivot]
    dg = pd.concat(pivotedCols + notPivotedCols, axis=1)
    dg.columns = columnsToPivot + columnsNotToPivot
    return dg


def pivotSeries(s, start, end): 
    """ start documenting this 
    """
    return pd.concat([s.shift(i) for i in range(start, end, -1)], axis=1).apply(lambda x: list(x), axis=1)


