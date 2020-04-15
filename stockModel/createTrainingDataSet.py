import pandas as pd
import numpy as np
import math as mt
from loadData.loadTimeSeries import loadTimeSeries

def createTrainingDataSet(stock, numSamples, endTime, pastStarts, futureEnds):
    """ document
    """
    dt = loadTimeSeries(stock, numSamples, endTime)
    dt['date']=dt.index
    X = _createFeaturesFromTimeSeries(dt, pastStarts)
    y = _createTargetFromTimeSeries(dt, futureEnds)
    X, y = _cleanTrainingData(X, y)
    return X, y

def createFeaturesAtCurrentTime(stock, currentTime, pastStarts):
    """ document
    """
    dt = loadTimeSeries(stock, pastStarts+1, currentTime)
    dt['date']=dt.index
    df = _createFeaturesFromTimeSeries(dt, pastStarts)
    validRows = df.date.apply(lambda x: (x[-1]-x[0]).min == len(x))
    df = df.loc[validRows]
    return df if len(df)!=1 else None


def _cleanTrainingData(X,y):
    """
    """
    validRowsX = X.date.apply(lambda x: (x[-1]-x[0]).min == len(x))
    validRowsY = y.date.apply(lambda x: (x[-1]-x[0]).min == len(x))
    validRows= validRowsX & validRowsY
    X, y = X.loc[validRows], y.loc[validRows]
    return X, y

def _createFeaturesFromTimeSeries(dt, pastStarts):
    """ start documenting this:
        Must be tested.
    """
    assert pastStarts>0, 'pastStart must be positive'
    df = _pivotWindow(dt, pastStarts, -1, ds.columns)
    return df

def _createTargetFromTimeSeries(dt, futureEnds):
    """ start documenting this
        Must be tested
    """
    assert futureEnds<0, 'futureEnds must be negative'
    df = _pivotWindow(dt, -1, futureEnds, dt.columns)
    nextMinuteValue =  df.consolidated.apply(lambda x:x[0])
    futureValue = df.consolidated.apply(lambda x:x[-1])
    t = (futureValue-nextMinuteValue)>0
    dtarget = pd.DataFrame({'target': t, 'date': df.date})
    return dtarget


def _pivotWindow(ds, start, end, columnsToPivot):
    """ start documenting this 
    """
    columnsNotToPivot = [col for col in ds.columns if col not in columnsToPivot]
    pivotedCols = [_pivotSeries(ds[col], start, end) for col in columnsToPivot]
    notPivotedCols = [ds[col] for col in columnsNotToPivot]
    dg = pd.concat(pivotedCols + notPivotedCols, axis=1)
    dg.columns = list(columnsToPivot) + columnsNotToPivot
    return dg


def _pivotSeries(s, start, end):
    """ start documenting this 
    """
    return pd.concat([s.shift(i) for i in range(start, end, -1)], axis=1).apply(lambda x: list(x), axis=1)