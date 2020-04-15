import pandas as pd
import numpy as np
from loadData.loadTimeSeries import loadTimeSeries

def createTrainingDataSet(stock, numSamples, currentTime, pastStarts, futureEnds):
    """ document
    """
    dt = loadTimeSeries(stock, numSamples, currentTime)
    dt['date']=dt.index
    X = _createFeaturesFromTimeSeries(dt, pastStarts)
    y = _createTargetFromTimeSeries(dt, futureEnds)
    X, y = _cleanTrainingData(X, y)
    return X, y

def createFeaturesAtCurrentTime(stock, currentTime, pastStarts):
    """ document
    """
    print('currentTime ', currentTime)
    dt = loadTimeSeries(stock, pastStarts+1, currentTime)
    dt['date']=dt.index
    print(dt.dtypes)
    print(dt)
    X = _createFeaturesFromTimeSeries(dt, pastStarts)
    print(X)
    X = _cleanFeatures(X)
    print(X)
    print('--------------')
    if len(X)!=1: return None
    if X.date.values[0][-1]!=(currentTime-timedelta(mins=1)): return None
    return X



def _cleanFeatures(X):
    correctLen = lambda x: False if (np.isnat(x[-0], dtype=np.datetime64) or np.isnat(x[-1], dtype=np.datetime64)) else (x[-1] - x[0]).minutes == len(x) - 1
    validRows = X.date.apply(correctLen)
    print('validRows')
    print(validRows)
    X = X.loc[validRows].copy()
    return X

def _cleanTrainingData(X,y):
    correctLen = lambda x: False if (np.isnat(x[-0], dtype=np.datetime64) or np.isnat(x[-1], dtype=np.datetime64)) else  (x[-1] - x[0]).minutes == len(x) - 1
    validRowsX = X.date.apply(correctLen)
    validRowsY = y.date.apply(correctLen)
    validRows= validRowsX & validRowsY
    X, y = X.loc[validRows], y.loc[validRows]
    return X, y

def _createFeaturesFromTimeSeries(dt, pastStarts):
    assert pastStarts>0, 'pastStart must be positive'
    df = _pivotWindow(dt, pastStarts, -1, dt.columns)
    return df

def _createTargetFromTimeSeries(dt, futureEnds):
    assert futureEnds<0, 'futureEnds must be negative'
    df = _pivotWindow(dt, -1, futureEnds, dt.columns)
    nextMinuteValue =  df.consolidated.apply(lambda x:x[0])
    futureValue = df.consolidated.apply(lambda x:x[-1])
    t = (futureValue-nextMinuteValue)>0
    dtarget = pd.DataFrame({'target': t, 'date': df.date})
    return dtarget


def _pivotWindow(ds, start, end, columnsToPivot):
    columnsNotToPivot = [col for col in ds.columns if col not in columnsToPivot]
    pivotedCols = [_pivotSeries(ds[col], start, end) for col in columnsToPivot]
    notPivotedCols = [ds[col] for col in columnsNotToPivot]
    dg = pd.concat(pivotedCols + notPivotedCols, axis=1)
    dg.columns = list(columnsToPivot) + columnsNotToPivot
    return dg

def _pivotSeries(s, start, end):
    return pd.concat([s.shift(i) for i in range(start, end, -1)], axis=1).apply(lambda x: list(x), axis=1)