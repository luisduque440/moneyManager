import pandas as pd

def pivotWindow(ds, start, end, columns = ['Open', 'High', 'Low', 'Close', 'Volume']):
    DateTime = pd.Series(ds.index, index=ds.index)
    validRow = (DateTime.shift(end+1)-DateTime.shift(start)).apply(lambda x: (start-end-1)==x.seconds/60)
    pivotedCols = [validRow] + [pivotSeries(ds[col], start, end) for col in columns] 
    dg = pd.concat(pivotedCols, axis=1)
    dg.columns = ['validRow'] + columns
    return dg

def pivotSeries(s, start, end): 
    return pd.concat([s.shift(i) for i in range(start, end, -1)], axis=1).apply(lambda x: list(x), axis=1)

def createTrainingDataSet(ds, numPastMins=5, numFutureMins=5):
    start, end = (numPastMins-1), -(numFutureMins+1) #(4,-6)
    df = pivotWindow(ds, start, -1) #[4,3,2,1,0]
    dt = pivotWindow(ds, -1, end, columns=['High']) #[-1,-2,-3,-4,-5]
    futureHigh = dt.High.apply(max)
    currentValue = df.Close.apply(lambda x: x[-1])
    df['target']= (futureHigh>currentValue)
    df['validTarget']=dt.validRow
    df = df[(df.validTarget==True) & (df.validRow==True)].drop(columns=['validTarget', 'validRow'])
    return df