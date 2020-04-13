import pandas as pd
import numpy as np
import math as mt


def createTargetOLD(barSeries, futureEnds=-20):
    """ An overly pesimistic buy-sell scenario
    Note: it is very dangerous to have a default value for future ends
    """
    assert futureEnds < 0, "futureEnds must be a negative integer"
    df = pd.DataFrame(
        {'future': barSeries.low.shift(futureEnds), 'nextMin': barSeries.high.shift(-1)},
        index=barSeries.index
    )
    target = df.apply(lambda x: np.nan if (mt.isnan(x.future) or mt.isnan(x.nextMin)) else (x.future > x.nextMin), axis=1)
    return target
