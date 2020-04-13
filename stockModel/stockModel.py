from stockModel.generatePipeline import generateLinearPipeline
from stockModel.createTrainingDataSet import createFeatures
from stockModel.createTrainingDataSet import createTrainingDataSet

class stockModel():
    """ Wrapper of a pipeline
    """
    def __init__( self, stock, pastStarts, futureEnds, trainSize):
        """ pastStarts: must be positive, number of days in the past used to create features
            futureEnds: must be negative, number of days in the future that we are trying to predict
        """
        self.stock = stock
        self.trainSize = trainSize
        self.pastStarts=pastStarts
        self.futureEnds=futureEnds 

    def predict_proba(self, currentTime):
        """ Method to be called every minute
        To do: if data is not 'reliable', return None
        """
        X = createFeatures(self.stock, self.pastStarts+1, currentTime, self.pastStarts)
        self.X = X.copy()   #debug
        return self.pipeline.predict_proba(X)[:,1][0]

    def fit(self, currentTime):
        """ Document asap
            There are at least two natural train-test splits to consider. Only considering one for now.
        """
        numSamples = self.trainSize + self.pastStarts - self.futureEnds
        X, y = createTrainingDataSet(stock, numSamples, currentTime, self.pastStarts, self.futureEnds)
        X, y = X[self.pastStarts: self.futureEnds], y[self.pastStarts: self.futureEnds].apply(bool)
        print("stockModel.untested() has not been untested... specifically check that createTrainindDataSet is not lecking data")
        self.pipeline = generateLinearPipeline()
        self.pipeline.fit(X, y)


    def modelThresholdWillbeValidInTheNearFuture(self, currentTime):
        """
        A method that checks how good the model works in the future. Only to be run during backtest.
        Add a warning.
        """
        pass



