

def dayTradingRoutine():
    """ This must start running at the beginning of the day
    """

    strategy = stockListTracker()
    lastTradedMinute = datetime.now().replace(hour=0, minute =0, second=0, microsecond=0)

    while(not marketClosedToday()):
        lastAvailableMinute = strategy.getLastTradeableMinute()
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
    # must check if the orders are not 'too old'. If they are we want to throw them away.
    
    return 



def produceDailyReport():
    """ produces a detailed report of what happened during the day
    """
    return "Daily Report"


def getCurrentMinute(timezone=None):
    cMinute = datetime.now()
    cMinute.replace(second=0, microsecond=0)
    return cMinute

def getTodayCloseTime(timezone=None):
    return datetime.now().replace(hour=16, minute =0, second=0, microsecond=0)

def getTodayOpenTime(timezone=None):
    return datetime.now().replace(hour=9, minute =0, second=0, microsecond=0)

def marketIsOpen():
    cTime = datetime.now()
    openTime = getTodayOpenTime()
    closeTime = getTodayCloseTime()
    return (cTime>=openTime and cTime<closeTime())

def marketClosedToday():
    cTime = datetime.now()
    closeTime = getTodayCloseTime()
    return cTime>=closeTime

