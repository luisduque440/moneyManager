from loadData.loadTimeSeries import getListOfAvailableStocks
from stockModel.createTrainingDataSet import createTarget

def _loadExpectedBuy(stocks=None, futureLen):
    """ gets Times in which it is a good idea to buyAndKeep for 20 mins
    """
    stocks=getListOfAvailableStocks() if stocks==None else stocks
    expectedBuy= {s:createTarget(stock, numSamples=None, currentTime=None, futureLen=futureLen) for s in stocks}
    return expectedBuy

def evaluateSuggestions(moneyManagerSuggestions, futureLen):
    """ document
    """
    buySuggestions = _getBuySuggestions(moneyManagerSuggestions)
    stocks = [s for s in buySuggestions]
    expectedBuy = _loadExpectedBuy(stocks, futureLen)
    goodBuyTimes = {s: set(s.loc[s== True].index) for s in expectedBuy.values()}

    totalCorrectBuySuggestions = sum([len([b for b in buySuggestions[s] if b in goodBuyTimes[s]]) for s in stocks])
    totalBuySuggestions = sum([len(buySuggestions[s]) for s in stocks])
    totalIdealBuyTimes = sum([len(goodBuyTimes[s]) for s in stocks])
    totalPossibleMovements = sum([len(expectedBuy[s]) for s in stocks])

    metrics = {
        'totalCorrectBuySuggestions': totalCorrectBuySuggestions,
        'totalBuySuggestions': totalBuySuggestions,
        'totalIdealBuyTimes':totalIdealBuyTimes,
        'totalPossibleMovements': totalPossibleMovements
    }
    return metrics


def _getBuySuggestions(moneyManagerSuggestions):
    """ document
    """
    buyMoneyManagerSuggestions = [b for b in moneyManagerSuggestions if b[0] == 'buyAndKeep20mins']
    buySuggestions = {}
    for s in self.stocks:
        buySuggestions[s] = {b[2] for b in buyMoneyManagerSuggestions if b[1] == s}
    return buySuggestions
