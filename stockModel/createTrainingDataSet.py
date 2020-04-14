import pandas as pd
import numpy as np
import math as mt
from loadData.loadTimeSeries import loadTimeSeries

def createTrainingDataSet(stock, numSamples, endTime, pastStarts, futureEnds):
    """ start documenting this 
    """
    X = createFeatures(stock, numSamples, endTime, pastStarts)
    y = createTarget(stock, numSamples, endTime, futureEnds)
    return X, y


def createFeatures(stock, numSamples, endTime, pastStarts):
    """ start documenting this:
        Must be tested.
    """
    assert pastStarts>0, 'pastStart must be positive'
    ds = loadTimeSeries(stock, numSamples, endTime)
    df = pivotWindow(ds, pastStarts, -1, ds.columns)
    return df


def createTarget(stock, numSamples, endTime, futureEnds):
    """ start documenting this
        Must be tested
    """
    assert futureEnds<0, 'futurEnds must be negative'
    ds = loadTimeSeries(stock, numSamples, endTime)
    dt = createTargetFromTimeSeries(ds, futureEnds)
    return dt


def createTargetFromTimeSeries(timeSeries, futureEnds):
    """ An overly pesimistic buy-sell scenario
    Note: it is very dangerous to have a default value for future ends
    """
    assert futureEnds < 0, "futureEnds must be a negative integer"
    df = pd.DataFrame(
        {'future': timeSeries.low.shift(futureEnds), 'nextMin': timeSeries.high.shift(-1)},
        index=timeSeries.index
    )
    target = df.apply(lambda x: np.nan if (mt.isnan(x.future) or mt.isnan(x.nextMin)) else (x.future > x.nextMin), axis=1)
    return target


def pivotWindow(ds, start, end, columnsToPivot):
    """ start documenting this 
    """
    columnsNotToPivot = [col for col in ds.columns if col not in columnsToPivot]
    pivotedCols = [pivotSeries(ds[col], start, end) for col in columnsToPivot]
    notPivotedCols = [ds[col] for col in columnsNotToPivot]
    dg = pd.concat(pivotedCols + notPivotedCols, axis=1)
    dg.columns = list(columnsToPivot) + columnsNotToPivot
    return dg


def pivotSeries(s, start, end): 
    """ start documenting this 
    """
    return pd.concat([s.shift(i) for i in range(start, end, -1)], axis=1).apply(lambda x: list(x), axis=1)
