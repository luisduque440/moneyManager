# we probably want to cache all the 'good' times to buy.

def evaluateAllSuggestions(suggestionList):
    pass


def evaluateSingleSuggestion(suggestion):
    pass

def evaluateAvailableSuggestions(self):
    """ document
    """
    buySuggestions = self._getBuySuggestions()
    idealBuyTimes = self._getIdealBuyTimes()
    correctBuySuggestions = {}
    for s in stocks:
        correctBuySuggestions[s] = [b for b in buySuggestions[s] if b in idealBuyTimes[s]]

    buySuggestionsCount = sum([len(buySuggestions[s]) for s in stocks])
    correctBuySuggestionsCount = sum([len(correctBuySuggestions[s]) for s in stocks])
    print(buySuggestionsCount, correctBuySuggestionsCount)

def _getBuySuggestions(self):
    """ document
    """
    managerSuggestions = [b for b in self.suggestions if b[0] == 'buyAndKeep20mins']
    buySuggestions = {}
    for s in self.stocks:
        buySuggestions[s] = {b[2] for b in managerSuggestions if b[1] == s}
    return buySuggestions

def _getIdealBuyTimes(self):
    """ gets Times in which it is a good idea to buyAndKeep for 20 mins
    """
    idealBuyTimes = {}
    for s in self.stocks:
        ds = loadTimeSeries(s)
        #dB = createTarget(ds) ############################# this function has changed
        #idealBuyTimes[s] = set(dB[dB == True].index)
    return idealBuyTimes





