import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from stockModel.generatePipeline import generateLinearPipeline

class stockModel():
    """Wrapper of a single pipeline with its respective thresholds, train datasets,  evaluators, performance
        Requirements:
            * The method
    """
    def __init__( self, stock, pastStarts=20, futureEnds=-20, trainSamples= 3000):
        """ pastStarts: must be positive, number of days in the past used to create features
            futureEnds: must be negative, number of days in the future that we are trying to predict
        """
        self.stock = stock
        self.trainSamples = trainSamples
        self.pastStarts=pastStarts
        self.futureEnds=futureEnds
        self.pipeline = generateLinearPipeline()


    def evaluate(self, currentTime): # needs change, seriously.
        """ Method to be called every minute.. NEEDS WORK !!!
        """
        pastDaysToLoad = 10 # this is (obviously) shady, some duplicated code !.
        trainStartDate = currentTime - timedelta(days=pastDaysToLoad)
        df = createTrainingDataSet(self.stock, trainStartDate, currentTime, self.pastStarts, self.futureEnds)
        X=df.drop(columns='target')
        lastScore = self.pipeline.predict_proba(X)[:,1][-1] 
        return lastScore

    def gatherTrainDataSet(self, currentTime):
        """ Document asap. NEEDS WORK !!!
        """
        pastDaysToLoad = 10 # this is (obviously) shady
        trainStartDate = currentTime - timedelta(days=pastDaysToLoad)
        df = createTrainingDataSet(self.stock, trainStartDate, currentTime, self.pastStarts, self.futureEnds)
        df = df.dropna()
        Xtrain=df[-self.trainSamples:].copy()
        ytrain = Xtrain.pop('target')
        return Xtrain, ytrain


    def train(self, currentTime):
        """ Document asap
        """
        Xtrain, ytrain = self.gatherTrainDataSet(currentTime)
        self.pipeline.fit(Xtrain, ytrain)
