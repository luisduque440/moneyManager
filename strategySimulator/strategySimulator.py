import pandas as pd
import random
import numpy as np
from datetime import datetime
from marketUtilities.loadTimeSeries import loadTimeSeries
from marketUtilities.loadTimeSeries import getListOfAvailableStocks
from marketUtilities.loadTimeSeries import loadPriceTimeSeries
from marketUtilities.marketSimulator import marketSimulator
from marketUtilities.marketSimulator import getPercentageOfIncreases

def strategySimulator(precision, recall, stocks, startDay, endDay, createTarget, numSimulations):
    """ Document this asap
    """
    outcomes = []
    numMovements = []
    positiveIncreasesPct = [] 
    for i in range(numSimulations):
        print('.', end ='')
        strategy =simulateSingleStrategy(precision, recall, stocks, startDay, endDay, createTarget)
        outcomes.append(marketSimulator(strategy).values[-1])
        numMovements.append(countPositionChanges(strategy))
        positiveIncreasesPct.append(getPercentageOfIncreases(strategy))
    return outcomes, numMovements, positiveIncreasesPct
    

def simulateSingleStrategy(precision, recall, stocks, startDay, endDay, createTarget):
    """ Notice that modelSuggestions are build from the modelOutcomes, they might be slightly different.
    """
    modelOutcomes = {s: simulateModelOutcome(precision, recall, s, startDay, endDay, createTarget) for s in stocks}
    modelSuggestions = {s : modelOutcomes[s].shift(1).fillna(False) for s in modelOutcomes}
    possibleMoves = getPossibleMoves(modelSuggestions)
    strategy= possibleMoves.apply(lambda x: random.choice(x) if len(x)>0 else None)
    strategy.values[0] = random.choice(stocks)
    strategy = keepPositionsForAtLeastNMins(strategy, N=20)
    return strategy

def simulateModelOutcome(precision, recall, stock, startDay, endDay, createTarget):
    """ Simulate the outcome of a single model.
    """
    barSeries = loadTimeSeries(stock, startDay, endDay)
    marketMinutes = barSeries.index
    idealPredictions = createTarget(barSeries)
    totalPositives = idealPredictions.value_counts()[True]
    positivesToChoose = int(totalPositives*recall/precision)
    truePositivesToChoose = int(precision*positivesToChoose)
    falsePositivesToChoose = positivesToChoose-truePositivesToChoose
    P = idealPredictions.values
    TP = random.choices([i for i in range(len(P)) if P[i]==True], k=truePositivesToChoose)
    FP = random.choices([i for i in range(len(P)) if P[i]==False], k=falsePositivesToChoose)
    PP = TP+FP
    
    numMinutes = len(idealPredictions)
    modelOutcome=[False for _ in range(numMinutes)]
    for p in PP:  
        modelOutcome[p]=True
    return pd.Series(modelOutcome, index=marketMinutes)


def getPossibleMoves(modelSuggestions):
    """ Notice that we need to compensate 
        Returns a list with the possible moves that the modelOutcomes suggest minute by minute, for example:
        [['GS', 'IBM'], [], [], ['GS'], ['GS'], ['GS'], [], [], ['IBM'], ...]
    """
    firstStock = list(modelSuggestions.keys())[0]
    marketMinutes = modelSuggestions[firstStock].index
    numMinutes=len(marketMinutes)
    possibleMoves=[[] for _ in range(numMinutes)]
    for stock in modelSuggestions:
        for i in range(numMinutes):
            if modelSuggestions[stock].values[i]:
                possibleMoves[i].append(stock)
    return pd.Series(possibleMoves, index=marketMinutes)


def keepPositionsForAtLeastNMins(strategy, N=20):
    """ Modifies a strategy so that each position is kept for at least N minutes
    """
    #strategy.values[i] = strategy.values[i-1] if strategy.values[i]==None else strategy.values[i]
    counter = 1 
    for i in range(1, len(strategy)):
        if strategy.values[i]==None:
            strategy.values[i]=strategy.values[i-1]
            counter+=1
        elif strategy.values[i]==strategy.values[i-1]:
            counter+=1
        else:
            if counter<N:
                strategy.values[i]=strategy.values[i-1]
                counter+=1
            else:
                counter=0
    return strategy


def countPositionChanges(strategy):
    """ Count the number of times that we need to buy/sell an asset
    """
    counter=0
    for i in range(1,len(strategy)):
        counter+=1 if strategy[i]!=strategy[i-1] else 0
    return counter


def getGainOfOnlyOneStockStrategy(stock, startDay, endDay):
    """ Gain==ROI (?)
    """
    marketTimes = loadTimeSeries(stock, startDay, endDay).index
    onlyOne = pd.Series([stock]*len(marketTimes), index=marketTimes)
    return marketSimulator(onlyOne, initialAmount=1)[-1]
