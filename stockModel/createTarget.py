
import pandas as pd
def createTarget(barSeries, futureEnds):
    """ An overly pesimistic buy-sell scenario
    ### this target MUST have np.nan, and it does not have it.... which is dangerous. !!!
    """
    assert futureEnds<0, "futurEnds must be a negative integer"
    d=(barSeries.low.shift(futureEnds)-barSeries.high.shift(-1))
    return (d>0)