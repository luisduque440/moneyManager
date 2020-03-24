import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from stockModel.generatePipeline import generateLinearPipeline
from stockModel.createTrainingDataSet import createTrainingDataSet
from loadData.loadTimeSeries import loadTimeSeries

class stockModel():
    """Wrapper of a single pipeline with its respective thresholds, train datasets,  evaluators, performance
        Requirements:
            * The method
    """
    def __init__( self, stock, pastStarts, futureEnds, trainSize):
        """ pastStarts: must be positive, number of days in the past used to create features
            futureEnds: must be negative, number of days in the future that we are trying to predict
        """
        self.stock = stock
        self.trainSize = trainSize
        self.pastStarts=pastStarts
        self.futureEnds=futureEnds
        self.pipeline = generateLinearPipeline()

    def evaluate(self, currentTime):
        """ Method to be called every minute
        """
        df = createTrainingDataSet(self.stock, self.pastStarts+1, currentTime, self.pastStarts, self.futureEnds)
        X=df.drop(columns='target')[-1:]
        self.X = X.copy()   # for debugging
        return self.pipeline.predict_proba(X)[:,1][0] 

    def train(self, currentTime):
        """ Document asap
        """
        Xtrain, ytrain = self.gatherTrainDataSet(currentTime)
        self.pipeline.fit(Xtrain, ytrain)


    def gatherTrainDataSet(self, currentTime):
        """ Document asap.
        """
        numSamples = self.trainSize+self.pastStarts-self.futureEnds
        df = createTrainingDataSet(self.stock, numSamples, currentTime, self.pastStarts, self.futureEnds)
        df = df[self.pastStarts: self.futureEnds]
        self.df = df.copy()    # for debugging
        X = df.copy()
        y = X.pop('target').apply(bool)
        return X, y



