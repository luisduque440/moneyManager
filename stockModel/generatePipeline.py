import numpy as np
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
from stockModel.createTrainingDataSet import createTrainingDataSet


def generateLinearPipeline():
    """ document.
    """
    cv = TimeSeriesSplit(n_splits=2)
    classifier = LogisticRegressionCV(penalty='l2', Cs = 10**np.linspace(-5,0,50), cv=cv, random_state=0, scoring='roc_auc', max_iter=1000)
    linearPipeline = generatePipeline(classifier)
    return linearPipeline


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