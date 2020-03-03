import pandas as pd
import random
import numpy as np
from datetime import datetime
from marketUtilities.loadTimeSeries import loadTimeSeries
from marketUtilities.loadTimeSeries import getListOfAvailableStocks
from marketUtilities.loadTimeSeries import loadPriceTimeSeries
from marketUtilities.marketSimulator import marketSimulator


def strategySimulator(precision, recall, stocks, startDay, endDay, createTarget, numSimulations):
    """ Document this asap
    """
    outcome = []
    numMovements = []
    for i in range(numSimulations):
        print(i, end =' ')
        strategy =simulateSingleStrategy(precision, recall, stocks, startDay, endDay, createTarget)
        outcome.append(marketSimulator(strategy).values[-1])
        numMovements.append(countPositionChanges(strategy))
    return outcome, numMovements
    

def simulateSingleStrategy(precision, recall, stocks, startDay, endDay, createTarget):
    """ Document Asap
    """
    modelOutcomes = {s: simulateModelOutcome(precision, recall, s, startDay, endDay, createTarget) for s in stocks}
    #print(modelOutcomes)
    possibleMoves = getPossibleMoves(modelOutcomes)
    #print(possibleMoves)
    strategy = generateStrategyFromPossibleMoves(possibleMoves, random.choice(stocks))
    #print(strategy)
    strategy = keepPositionsForAtLeastNMins(strategy, N=20)
    marketMinutes = loadTimeSeries(stocks[0], startDay, endDay).index
    strategy = pd.Series(strategy, index=marketMinutes)
    return strategy


def simulateModelOutcome(precision, recall, stock, startDay, endDay, createTarget):
    """ Simulate the outcome of a single model.
    """
    price = loadTimeSeries(stock, startDay, endDay).consolidated
    idealPredictions = createTarget(price)
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
    return modelOutcome


def getPossibleMoves(modelOutcomes):
    """ Returns a list with the possible moves that the modelOutcomes suggest minute by minute, for example:
        [['GS', 'IBM'], [], [], ['GS'], ['GS'], ['GS'], [], [], ['IBM'], ...]
    """
    firstStock = list(modelOutcomes.keys())[0]
    numMinutes=len(modelOutcomes[firstStock])
    possibleMoves=[[] for _ in range(numMinutes)]
    for stock in modelOutcomes:
        for i in range(numMinutes):
            if modelOutcomes[stock][i]:
                possibleMoves[i].append(stock)
    return possibleMoves


def generateStrategyFromPossibleMoves(possibleMoves, firstPosition):
    """ Picks a single strategy at random from a list with possibleMoves
    """
    numMinutes = len(possibleMoves)
    strategy = [None for _ in range(numMinutes)]
    strategy[0] = firstPosition
    for i in range(1, len(strategy)):
        if len(possibleMoves[i])==0:
            strategy[i]=strategy[i-1]
        else:
            strategy[i] = random.choice(possibleMoves[i])
    return strategy

def keepPositionsForAtLeastNMins(strategy, N=20):
    """ Modifies a strategy so that each position is kept for at least N minutes
    """
    counter = 1 
    for i in range(1, len(strategy)):
        if strategy[i]==strategy[i-1]:
            counter+=1
        else:
            if counter<N:
                strategy[i]=strategy[i-1]
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


def testCaseForModelSimulator(STOCK):
    """ 
    Ugly and temporal !
    Use the following in test_marketSimulator.py .... repeated but used in the notebook
    Not even sure about what I want to do with this, or why is this here
    """
    S=loadTimeSeries(STOCK, datetime(2019,1,1), datetime(2020,1,1)).consolidated
    positionTS=pd.Series([STOCK]*len(S),index=S.index)
    win = marketSimulator(positionTS, initialAmount=1)
    return win.values[-1]