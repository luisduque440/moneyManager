import pandas as pd
import numpy as np
from datetime import datetime
from loadData.loadTimeSeries import loadTimeSeries
from modeling.createTarget import createTarget

def createTrainingDataSet(stock1, numSamples, endTime, pastStarts, futureEnds):
    """ start documenting this 
    """
    assert pastStarts>0, 'pastStart must be positive'
    assert futureEnds<0, 'futurEnds must be negative'
    ds = loadTimeSeries(stock1, numSamples, endTime)
    ds['target'] = createTarget(ds, futureEnds)
    columnsToPivot = list(ds.columns)
    columnsToPivot.remove('target')
    df = pivotWindow(ds, pastStarts, -1, columnsToPivot)
    return df


def pivotWindow(ds, start, end, columnsToPivot):
    """ start documenting this 
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


