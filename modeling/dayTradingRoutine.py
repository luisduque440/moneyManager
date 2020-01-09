import os, time
from .stockListTracker import stockListTracker
from datetime import datetime as dt
os.environ["TZ"] = "America/New_York"


def dayTradingRoutine():
    """ This must start running at the beginning of the day
    """

    strategy = stockListTracker()
    lastTradedMinute = dt.now().replace(hour=0, minute =0, second=0, microsecond=0)

    while(not marketClosedToday()):
        lastAvailableMinute = strategy.getLastTradeableMinute() # getLastMinuteDataIsAvailable()
        if lastAvailableMinute>lastTradedMinute:
            orders = strategy.getExecutableOrders()
            executeOrders(orders)
            lastTradedMinute = lastAvailableMinute
        break

    produceDailyReport()
    print("--- end of daily trading routine ---")



def executeOrders(orders):
    """ Execute a dictionary with orders
    """
    # must check if the orders are not 'too old'. If they are we should throw them away.
    
    return 



def produceDailyReport():
    """ produces a detailed report of what happened during the day
    """
    return 


def getCurrentMinute(timezone=None):
    """
    """
    cMinute = dt.now()
    cMinute.replace(second=0, microsecond=0)
    return cMinute

def getTodayCloseTime(timezone=None):
    return dt.now().replace(hour=16, minute =0, second=0, microsecond=0)

def getTodayOpenTime(timezone=None):
    return dt.now().replace(hour=9, minute =0, second=0, microsecond=0)

def marketIsOpen():
    cTime = dt.now()
    openTime = getTodayOpenTime()
    closeTime = getTodayCloseTime()
    return (cTime>=openTime and cTime<closeTime())

def marketClosedToday():
    cTime = dt.now()
    closeTime = getTodayCloseTime()
    return cTime>=closeTime

