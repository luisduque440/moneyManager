import pandas as pd
from datetime import timedelta
from loadData.loadTimeSeries import loadTimeSeries


def createTrainingDataSet(stock, numSamples, currentTime, pastLen, futureLen, dropDateColumns=True):
    """ document
    """
    X = createFeatures(stock, numSamples, currentTime, pastLen, dropDateColumns)
    y = createTarget(stock, numSamples, currentTime, futureLen, dropDateColumns)
    X, y = _keepRowsWithIndexesInBoth(X, y)
    return X, y


def createFeaturesAtCurrentTime(stock, currentTime, pastLen, dropDateColumns=True):
    """ document
    """
    X = createFeatures(stock, pastLen, currentTime, pastLen, dropDateColumns)
    if len(X)!=1: return None
    if X.index[0]!=currentTime: return None
    return X


def createFeatures(stock, numSamples, currentTime, pastLen, dropDateColumns=True):
    """ document
    """
    assert pastLen > 0, 'pastLen must be positive'
    dt = loadTimeSeries(stock, numSamples, currentTime)
    dt['date'] = dt.index
    X = _pivotWindow(dt, pastLen-1, -1, dt.columns)
    lastFeatureDatePlusOneMinute = X.date.apply(lambda x: x[-1]).apply(lambda x:x+timedelta(minutes=1))
    X.index = lastFeatureDatePlusOneMinute
    X = _keepRowsWithoutNaT(X)
    if dropDateColumns: X=X.drop(columns='date')
    return X

def createTarget(stock, numSamples, currentTime, futureLen, dropDateColumns=True):
    """ document
    """
    assert futureLen > 0, 'futureLen must be positive'
    dt = loadTimeSeries(stock, numSamples, currentTime)
    dt['date'] = dt.index
    df = _pivotWindow(dt, -1, -futureLen-1, dt.columns)
    firstMinuteValue =  df.consolidated.apply(lambda x:x[0])
    lastMinuteValue = df.consolidated.apply(lambda x:x[-1])
    t = (lastMinuteValue-firstMinuteValue)>0
    y = pd.DataFrame({'target': t, 'date': df.date})
    firstMinuteDateTime = y.date.apply(lambda x: x[0]).values
    y.index = firstMinuteDateTime
    y = _keepRowsWithoutNaT(y)
    if dropDateColumns: y = y.drop(columns='date').target
    return y



def _keepRowsWithIndexesInBoth(X,y):
    idx = X.index.intersection(y.index)
    return X.loc[idx].copy(), y.loc[idx].copy()


def _keepRowsWithoutNaT(df):
    hasNulls = lambda x: len([t for t in x if pd.isnull(t)]) > 0
    minutes = lambda x: (x[-1] - x[0]).seconds // 60
    correctLen = lambda x: False if hasNulls(x) else (minutes(x) == len(x) - 1)
    validRows = df.date.apply(correctLen)
    df = df.loc[validRows].copy()
    return df


def _pivotWindow(ds, start, end, columnsToPivot):
    columnsNotToPivot = [col for col in ds.columns if col not in columnsToPivot]
    pivotedCols = [_pivotSeries(ds[col], start, end) for col in columnsToPivot]
    notPivotedCols = [ds[col] for col in columnsNotToPivot]
    dg = pd.concat(pivotedCols + notPivotedCols, axis=1)
    dg.columns = list(columnsToPivot) + columnsNotToPivot
    return dg


def _pivotSeries(s, start, end):
    return pd.concat([s.shift(i) for i in range(start, end, -1)], axis=1).apply(lambda x: list(x), axis=1)