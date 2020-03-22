import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import TimeSeriesSplit
from sklearnUtilities.preprocessors import ColumnSelector
from sklearnUtilities.preprocessors import timeSeriesScaler
from sklearnUtilities.preprocessors import timeSeriesToFeatures 
from sklearnUtilities.preprocessors import createTimeFeatures 
from sklearnUtilities.preprocessors import TransformationWrapper
from sklearnUtilities.preprocessors import BayesianCategoricalEncoder
from sklearnUtilities.preprocessors import bayesianTransformer
from sklearnUtilities.preprocessors import createTimeSeriesDiferences
from sklearnUtilities.preprocessors import FunctionTransformer
from sklearnUtilities.precisionRecallUtilities import selectThreshold
from modeling.createTrainingDataSet import createTrainingDataSet



class StockModel():
    """Wrapper of a single pipeline with its respective thresholds, train datasets,  evaluators, performance
        Requirements:
            * The method
    """
    def __init__( self, stock, pastStarts=20, futureEnds=-20, trainSamples= 3000):
        """ pastStarts: must be positive, number of days in the past used to create features
            futureEnds: must be negative, number of days in the future that we are trying to predict
        """
        cv = TimeSeriesSplit(n_splits=2)
        classifier = LogisticRegressionCV(penalty='l2', Cs = 10**np.linspace(-5,0,50), cv=cv, random_state=0, scoring='auc')
        self.stock = stock
        self.trainSamples = trainSamples
        self.pastStarts=pastStarts
        self.futureEnds=futureEnds
        self.pipeline = self.generatePipeline(classifier)


    def evaluate(self, currentTime): # needs change, seriously.
        """ This function should be called every minute ...
        """
        pastDaysToLoad = 10 # this is (obviously) shady
        df = createTrainingDataSet(self.stock, trainStartDate, currentTime, self.pastStarts, self.futureEnds)
        X=df.drop(columns='target')
        lastScore = self.pipeline.predict_proba(X)[:,1][-1] 
        return lastScore

    def gatherTrainDataSet(self, currentTime):
        """ Document asap
        """
        pastDaysToLoad = 10 # this is (obviously) shady
        trainStartDate = currentTime - timedelta(days=pastDaysToLoad)
        df = createTrainingDataSet(self.stock, trainStartDate, currentTime, self.pastStarts, self.futureEnds)
        df = df.dropna()
        Xtrain=df[-self.trainSamples:].copy()
        ytrain = Xtrain.pop('target')
        return Xtrain, ytrain


    def train(self):
        """ Always picks the model witht he biggest auc, does not care about thresholds
        """
        Xtrain, ytrain = self.gatherTrainDataSet()
        self.pipeline.fit(Xtrain, ytrain)


def generatePipeline(classifier):
	
    """ start documenting this 
    To do:
        0) The name of this should change: generateTimeSeriesPipeline()
        1) classifier could be a parameter, columns to use could be parameters
        2) Include differences as features too.
        3) Bayes-encode the time features
        4) How should the exogenous features feed this pipeline?
    """
    pipeline = Pipeline([
        ('selectcolumns', ColumnSelector()), 
        ('scaletimeseries', FunctionTransformer(timeSeriesScaler)),
        ('createdifferences', FunctionTransformer(createTimeSeriesDiferences)), 
        ('timeSeriesToFeatures', FunctionTransformer(timeSeriesToFeatures)),
        ('createtimefeatures', FunctionTransformer(createTimeFeatures)),
        ('fillemptyvalues', TransformationWrapper(SimpleImputer(strategy='median'))),
        ('scaler', TransformationWrapper(MinMaxScaler())),
        ('classifier', classifier)
        
    ])
    return pipeline
