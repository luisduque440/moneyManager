
import pandas as pd
import numpy as np
import math as mt
def createTarget(barSeries, futureEnds):
    """ An overly pesimistic buy-sell scenario
    """
    assert futureEnds<0, "futurEnds must be a negative integer"
    df = pd.DataFrame(
			{'future': barSeries.low.shift(futureEnds), 'nextMin': barSeries.high.shift(-1)}, 
			index=barSeries.index
    	)
    target = df.apply(lambda x: np.nan if (mt.isnan(x.future) or mt.isnan(x.nextMin)) else (x.future>x.nextMin), axis=1)
    return target