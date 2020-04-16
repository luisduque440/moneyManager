import pandas as pd
from datetime import timedelta
from loadData.loadTimeSeries import loadTimeSeries

def createTrainingDataSet(stock, numSamples, currentTime, pastLen, futureLen):
    """ document
    """
    assert pastLen>0, 'pastLen must be positive'
    assert futureLen>0, 'futureLen must be positive'
    dt = loadTimeSeries(stock, numSamples, currentTime)
    dt['date']=dt.index
    X = _createFeaturesFromTimeSeries(dt, pastLen)
    y = _createTargetFromTimeSeries(dt, futureLen)
    X, y = _cleanTrainingData(X, y)
    firstFutureDate = y.date.apply(lambda x: x[0]).values
    y.index = firstFutureDate
    X.index = firstFutureDate
    return X, y

def createFeaturesAtCurrentTime(stock, currentTime, pastLen):
    """ document
    """
    dt = loadTimeSeries(stock, pastLen, currentTime)
    dt['date']=dt.index
    X = _createFeaturesFromTimeSeries(dt, pastLen)
    X = _cleanFeatures(X)
    if len(X)!=1: return None
    lastDateInFeatures = X.date.values[0][-1]
    if lastDateInFeatures!=(currentTime-timedelta(minutes=1)): return None
    X.index=[lastDateInFeatures+timedelta(minutes=1)]
    return X

_hasNulls= lambda x: len([t for t in x if pd.isnull(t)])>0
_minutes = lambda x: (x[-1] - x[0]).seconds//60
_correctLen = lambda x: False if _hasNulls(x) else (_minutes(x)== len(x) - 1)

def _cleanFeatures(X):
    validRows = X.date.apply(_correctLen)
    X = X.loc[validRows].copy()
    return X

def _cleanTrainingData(X,y):
    validRowsX = X.date.apply(_correctLen)
    validRowsY = y.date.apply(_correctLen)
    validRows= validRowsX & validRowsY
    X, y = X.loc[validRows], y.loc[validRows]
    return X, y

def _createFeaturesFromTimeSeries(dt, pastLen):
    df = _pivotWindow(dt, pastLen-1, -1, dt.columns)
    return df

def _createTargetFromTimeSeries(dt, futureLen):
    df = _pivotWindow(dt, -1, -futureLen-1, dt.columns)
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