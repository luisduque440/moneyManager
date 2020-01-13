
def OLDcreateTrainingDataSet(ds, presentStart=1, pastStart=4, futureEnd=-5):
    """ start documenting this 
        To do: A more realistic target: the difference between next minutes price and the price in 20 minutes.
    """
    assert (pastStart>=0 and futureEnd<0 and presentStart>=0), "check the signs of the specified times"
    df = pivotWindow(ds, pastStart, -1) #[4,3,2,1,0] # (looks at past and present)
    dpresent = pivotWindow(ds, presentStart, -1, columns=['Low', 'High']) # [1, 0] # hardcoded for now: two minutes
    dfuture = pivotWindow(ds, -1, futureEnd, columns=['Low', 'High']) #[-1,-2,-3,-4,-5] (looks at the future)
    df['futureAverage'] = (dfuture.Low+dfuture.High).apply(np.mean)
    df['presentAverage'] = (dpresent.Low+dpresent.High).apply(np.mean)
    df['futureValid'] = dfuture.validRow
    df['presentValid'] = dpresent.validRow
    df['unthresholdedTarget']= (df.futureAverage-df.presentAverage).div(df.presentAverage)
    targetThreshold = np.percentile(df.unthresholdedTarget.dropna(), 50) 
    df['target'] = df.unthresholdedTarget>targetThreshold
    df= df[(df.validRow==True) & (df.futureValid==True) & (df.presentValid==True)]
    df = df.drop(columns=['validRow', 'futureValid', 'presentValid', 'futureAverage', 'presentAverage', 'unthresholdedTarget'])
    return df