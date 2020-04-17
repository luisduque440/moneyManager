from loadData.loadTimeSeries import getListOfAvailableStocks
from stockModel.createTrainingDataSet import createTarget

def _getIdealBuyTimes(stocks=None):
    """ gets Times in which it is a good idea to buyAndKeep for 20 mins
    """
    stocks=getListOfAvailableStocks() if stocks==None else stocks
    idealBuyTimes = {}
    for s in stocks:
        dB = createTarget(stock, numSamples=None, currentTime=None, futureLen):
        idealBuyTimes[s] = set(dB[dB == True].index)
    return idealBuyTimes


idealBuyTimes = _getIdealBuyTimes()
def evaluateSuggestions(moneyManagerSuggestions):
    """ document
    """
    idealBuyTimes = _getIdealBuyTimes()
    buySuggestions = _getBuySuggestions(moneyManagerSuggestions)
    correctBuySuggestions = {}
    for s in stocks:
        correctBuySuggestions[s] = [b for b in buySuggestions[s] if b in idealBuyTimes[s]]

    buySuggestionsCount = sum([len(buySuggestions[s]) for s in stocks])
    correctBuySuggestionsCount = sum([len(correctBuySuggestions[s]) for s in stocks])
    print(buySuggestionsCount, correctBuySuggestionsCount)


# maybe money manager could do this already, makes no sense to have this separated.
# also no point of stockModel also returning the label of the stock its recommending to buy, thats silly.
# Maybe not.
def _getBuySuggestions(moneyManagerSuggestions):
    """ document
    """
    buyMoneyManagerSuggestions = [b for b in self.suggestions if b[0] == 'buyAndKeep20mins']
    buySuggestions = {}
    for s in self.stocks:
        buySuggestions[s] = {b[2] for b in buyMoneyManagerSuggestions if b[1] == s}
    return buySuggestions
