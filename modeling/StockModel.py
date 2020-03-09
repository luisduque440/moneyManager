from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
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
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA



class stockModel():
    """Wrapper of a single pipeline with its respective thresholds, train datasets,  evaluators, performance
        Requirements:
            * Data is fed to this class minute by minute in chronological order.
            * The model automatically decides to retrain itself when results are 'no longer satisfyin expectations'
            * The way in which the previous point should be implemented involves looking at thresholds in a Bayesian way. 
            * It is unreallistic to assume that the model is going to start the day behaving as it behave by the end of last day.

    """
    def __init__(self, stock, requiredTrainingSamples= 3000, requiredEvaluationSamples=200, 
    				   requiredPrecision=0.55, requiredRecall=0.5, requiredCertainty=0.9):

        self.stock = stock
        self.requiredTrainingSamples = requiredTrainingSamples
        self.requiredEvaluationSamples = requiredEvaluationSamples
        self.requiredPrecision = requiredPrecision 
        self.requiredRecall = requiredRecall 
        self.requiredCertainty = requiredCertainty


    def getModelSuggestion(self, currentTime):
        """ This function should be called every minute
        """
        self.currentTime=currentTime
        if self.modelRequiresTraining(): self.train()
        self.getModelThreshold()
        modelSuggestsToBuy = self.modelIsValid() and self.thresholdedOutput()
        order=self.generateBuyOrder() if modelSuggestsToBuy else self.generateNullOrder()
        return order 





    def train(self):
        """
        """
        self.modelDate=self.currentTime
        Xtrain, ytrain = self.gatherTrainDataSet()
        Xeval, yeval = self.gatherEvaluationDataSet()
        classifiers = [
            BernoulliNB(), 
            LogisticRegression(penalty='none'), 
            LogisticRegressionCV(penalty='l1', Cs = 10**np.linspace(-4,1,50),  cv=5, random_state=0), 
            LogisticRegressionCV(penalty='l2', Cs = 10**np.linspace(-5,0,100), cv=5, random_state=0)
        ]

        #import numpy as np
        #from sklearn.metrics import roc_auc_score
        #y_true = np.array([0, 0, 1, 1])
        #y_scores = np.array([0.1, 0.4, 0.35, 0.8])
        #roc_auc_score(y_true, y_scores)

        pipelines = [generatePipeline(clf) for clf in classifiers]
        for p in pipelines: pl.fit(Xtrain, ytrain)
        areasUnderCurves = [auc(clf, Xeval, yeval) for p in pipelines]
        self.model = pipelines[np.argmax(areasUnderCurves)]

    def modelIsValid(self):
        """ A model is valid if the following happens:
            (1) The threshold is valid: i.e. we precision, recall and alpha are big enough
            (2) We are not at the beginning of the day (?)
        """
    	return True

    def getModelThreshold(self):
        """ Implemented somewherelse
        """
        return 

    def thresholdedOutput(self):
    	return 

    def modelRequiresTraining(self):
        """ Still not very well defined
        """
    	return

    def getTrainDataSet(self):
        Xtrain=None
        ytrain=None
        return Xtrain, ytrain

    def getEvaluationDataSet(self):
        Xeval=None
        yeval=None
        return Xeval, yeval


    def generateBuyOrder(self):
        buyOrder =  {'orderType': 'BUY', 
                'stock': self.stock,  
                'generatedAt': datetime.now(), 
                'expiresAt': datetime(2040,1,1),
                'precision': 0.666,
                'recall': 0.222}
        return buyOrder


    def generateNullOrder(self):
        buyOrder =  {'orderType': 'NULL', 
                'stock': self.stock,  
                'generatedAt': datetime.now(), 
                'expiresAt': datetime(2040,1,1),
                'precision': 0.666,
                'recall': 0.222}
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
        #('pca', TransformationWrapper(PCA(n_components=30), colnames=['PC_'+str(i) for i in range(1,31)])),
        ('scaler', TransformationWrapper(MinMaxScaler())),
        ('classifier', classifier)
        
    ])
    return pipeline







#X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
#pca = PCA(n_components=2)
#('scaletimeseries', FunctionTransformer(timeSeriesScaler)),


