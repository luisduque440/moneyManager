import pandas as pd
import random
import numpy as np
from datetime import datetime
from marketUtilities.loadTimeSeries import loadTimeSeries
from marketUtilities.loadTimeSeries import getListOfAvailableStocks
from marketUtilities.loadTimeSeries import loadPriceTimeSeries
from marketUtilities.marketSimulator import marketSimulator

priceTimeSeries = loadPriceTimeSeries()
bestPossiblePredictions = {stock: priceTimeSeries[stock].shift(-20)>priceTimeSeries[stock].shift(-1) for stock in priceTimeSeries}    

def simulateStrategyMultipleTimes(precision, recall, availableStocks, numSimulations):
    outcome = []
    numMovements = []
    for i in range(numSimulations):
        strategy =strategySimulatorWithMultipleStocks(precision, recall, availableStocks)
        outcome.append(marketSimulator(strategy).values[-1])
        numMovements.append(countPositionChanges(strategy))
    return outcome, numMovements
    
def strategySimulatorWithMultipleStocks(precision, recall, availableStocks, startTime=datetime(2019,1,1), endTime=datetime(2020,1,1)):
    """
       We are loading/using all bestPossiblePredictions ... maybe we should not
       this probably only works with the default startTime and endTIme
    """
    availableMarketMinutes = loadTimeSeries('GS').index
    strategyTimes = [t for t in availableMarketMinutes if t>=startTime and t<endTime]
    possibleMoves=[[] for _ in range(len(strategyTimes))]
    
    for stock in availableStocks:
        
        allPositives = bestPossiblePredictions[stock].value_counts()[True]
        predictedPositives = int(allPositives*recall/precision)
        truePositives = int(precision*predictedPositives)
        P = bestPossiblePredictions[stock].values
        TP = random.choices([i for i in range(len(P)) if P[i]==True], k=truePositives)
        FP = random.choices([i for i in range(len(P)) if P[i]==False], k=predictedPositives-truePositives)
        PP = TP+FP
        for p in PP:possibleMoves[p].append(stock)

    strategy = [None for _ in range(len(strategyTimes))]
    strategy[0] = random.choice(availableStocks)
    for i in range(1, len(strategy)):
        if len(possibleMoves[i])==0:
            strategy[i]=strategy[i-1]
        else:
            strategy[i] = random.choice(possibleMoves[i])
            
    
    counter = 1 # force our positions to be held for at least 20 minutes
    for i in range(1, len(strategy)):
        if strategy[i]==strategy[i-1]:
            counter+=1
        else:
            if counter<20:
                strategy[i]=strategy[i-1]
                counter+=1
            else:
                counter=0
    
    
    strategy=pd.Series(strategy, index=strategyTimes)
    return strategy


def countPositionChanges(strategy):
    counter=0
    for i in range(1,len(strategy)):
        counter+=1 if strategy[i]!=strategy[i-1] else 0
    return counter



# Use the following in test_marketSimulator.py .... repeated but used in the notebook
def testCaseForModelSimulator(STOCK):
    S=loadTimeSeries(STOCK, datetime(2019,1,1), datetime(2020,1,1)).consolidated
    positionTS=pd.Series([STOCK]*len(S),index=S.index)
    win = marketSimulator(positionTS, initialAmount=1)
    return win.values[-1]