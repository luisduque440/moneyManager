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
from sklearnUtilities.modeling import createTrainingDataSet



class stockModel():
    """Wrapper of a single pipeline with its respective thresholds, train datasets,  evaluators, performance
        Requirements:
            * Data is fed to this class minute by minute in chronological order.
            * The model automatically decides to retrain itself when results are 'no longer satisfyin expectations'
            * The way in which the previous point should be implemented involves looking at thresholds in a Bayesian way. 
            * It is unreallistic to assume that the model is going to start the day behaving as it behave by the end of last day.

    """
    def __init__( self, stock, pastStarts, futureEnds, 
            requiredTrainingSamples= 3000, requiredEvaluationSamples=200, 
            requiredPrecision=0.55, requiredRecall=0.5, requiredCertainty=0.9):
        """ pastStarts: must be positive, number of days in the past used to create features
            futureEnds: must be negative, number of days in the future that we are trying to predict

        """

        self.stock = stock
        self.requiredTrainingSamples = requiredTrainingSamples
        self.requiredEvaluationSamples = requiredEvaluationSamples
        self.requiredPrecision = requiredPrecision 
        self.requiredRecall = requiredRecall 
        self.requiredCertainty = requiredCertainty


    def getModelSuggestion(self, currentTime):
        """ This function should be called every minute
        """
        self.currentTime = currentTime
        self.gatherTrainEvalDataSets()
        self.threshold = self.getModelThreshold()
        
        if self.modelRequiresTraining(): 
            self.train()

        order=self.generateBuyOrder() if self.thresholdedOutput() else self.generateNullOrder()
        return order 

    def gatherTrainEvalDataSets(self):
        """ 
            To do:
            * We might want check the quality of the sets we gathered (specially if there are missing values)
            * We might want to delete the rows with empty values in certain cirtumstances
        """
        pastDaysToLoad = 10 # this is (obviously) shady
        trainStartDate = self.currentTime - timedelta(days=1)
        df = createTrainingDataSet(self.stock, trainStarts, self.currentTime):
        trainStartsSample = -self.requiredTrainingSamples - self.requiredEvaluationSamples
        evaluationStartsSample = - self.requiredEvaluationSamples
        self.Xtrain=df[trainStartsSample:evaluationStartsSample].copy()
        self.ytrain=self.Xtrain.pop('target')
        self.Xeval=df[evaluationStartsSample:].copy()
        self.yeval=self.Xeval.pop('target')


    def train(self):
        """ Always picks the model witht he biggest auc, does not care about thresholds
        """
        self.modelDate = self.currentTime
        cv = TimeSeriesSplit(n_splits=2)
        classifiers = [
            BernoulliNB(), 
            LogisticRegression(penalty='none'), 
            LogisticRegressionCV(penalty='l1', Cs = 10**np.linspace(-4,1,50),  cv=cv, random_state=0, scoring='auc'), 
            LogisticRegressionCV(penalty='l2', Cs = 10**np.linspace(-5,0,50), cv=cv, random_state=0, scoring='auc')
        ]

        pipelines = [generatePipeline(clf) for clf in classifiers]
        for p in pipelines: pl.fit(self.Xtrain, self.ytrain)
        areasUnderCurves = [roc_auc_score(yeval, p.predict_proba(self.Xeval)[:,1]) for p in pipelines]
        self.model = pipelines[np.argmax(areasUnderCurves)]


    def modelRequiresTraining(self):
        """ 
        To do:
            * Alternative way: many heuristics can be tried here, depending on if/how model is valid working.
        """
        if self.threshold==None and self.modelHasNotBeenTrainedInAWhile():
            return True
        return False


    def getModelThreshold(self):
        """ Returns None if its not possible to satisfy the requirements
            Somehow this piece of the puzzle does not feel entirely right.
            This cannot be right, very careful!!
            Track empty values on yeval, ytrain ... those are key, I bet.
        """
        scores = self.model.predict_proba(self.Xeval)[:,1]
        p,r,threshold,a = selectThreshold(self.yeval, scores, self.requiredPrecision, self.requiredRecall, self.requiredCertainty)
        return threshold

    def thresholdedOutput(self):
        """ Somehow this piece of the puzzle does not feel entirely right.
            This cannot be right, very careful!!
            Track empty values on yeval, ytrain ... those are key, I bet.
            Xeval, yeval, Xtrain, ytrain must be exposed even just for debugging purposes.
        """
        if self.threshold==None:
            return None
        scores = self.model.predict_proba(self.Xeval)[:,1]
    	return scores[-1]>self.threshold


    def generateBuyOrder(self):
        buyOrder =  {
            'orderType': 'BUY', 
            'stock': self.stock,  
            'generatedAt': datetime.now(), 
            'expiresAt': self.currentTime + timedelta(minute=1)
        }
        return buyOrder


    def generateNullOrder(self):
        buyOrder =  {
            'orderType': 'NULL', 
            'stock': self.stock,  
            'generatedAt': datetime.now(), 
            'expiresAt': self.currentTime + timedelta(minute=1)
        }
        return buyOrder



#('classifier', LogisticRegression(penalty='none', solver='sag', max_iter=1000))
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

#('pca', TransformationWrapper(PCA(n_components=30), colnames=['PC_'+str(i) for i in range(1,31)])),
#('scaletimeseries', FunctionTransformer(timeSeriesScaler)),





