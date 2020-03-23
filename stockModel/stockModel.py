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
        df = createTrainingDataSet(self.stock, self.pastStarts, currentTime, self.pastStarts, self.futureEnds)
        df=df.drop(columns='target')
        df = df[-1:]
        return self.pipeline.predict_proba(X)[:,1][0] 

    def train(self, currentTime):
        """ Document asap
        """
        Xtrain, ytrain = self.gatherTrainDataSet(currentTime)
        self.pipeline.fit(Xtrain, ytrain)


    def gatherTrainDataSet(self, currentTime):
        """ Document asap. NEEDS WORK !!!
        """
        df = createTrainingDataSet(self.stock, self.trainSize, currentTime, self.pastStarts, self.futureEnds)
        self.df = df.copy() # just for debugging
        Xtrain = df.copy()
        ytrain = Xtrain.pop('target') ### this target MUST have np.nan, and it does not have it.
        return Xtrain, ytrain



