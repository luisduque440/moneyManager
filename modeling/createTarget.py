
import pandas as pd
def createTarget(barSeries, memSize=120):
    """ An overly pesimistic buy-sell scenario
    """
    d=(barSeries.low.shift(-20)-barSeries.high.shift(-1))
    return (d>0)