import pandas as pd
import numpy as np
from datetime import datetime
from .loadTimeSeries import loadTimeSeries

def createTrainingDataSet(stock1, startDay, endDay, pastStart=20):
    """ Start documenting now.
        This requires more defensive code: look for instance at the old implementation of this function.
    """
    ds = loadTimeSeries(stock1, startDay, endDay)

    # The following target gives very good performance (probably useless)
    #s = ds.drop(columns='volume').apply(np.mean, axis=1)
    #ds['target'] = (s.shift(-1)>s.shift(0))

    # The following work once we included time features, we might not be overfitting.
    # (this is the one that is working the best so far)
    #ds['target']=ds.open_price.shift(-1)<ds.close_price.shift(-1)

    # January 28: This one works, it is possible to spot a signal with L2 regularization
    ds['target'] = (ds.consolidated.shift(-20)>ds.consolidated.shift(-1))


    # January 28: If this one works, our simulations would get easier!
    #ds['target'] = (ds.consolidated.shift(-2)>ds.consolidated.shift(-1))

    columnsToPivot = list(ds.columns)
    columnsToPivot.remove('target')
    df = pivotWindow(ds, pastStart, -1, columnsToPivot)
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


