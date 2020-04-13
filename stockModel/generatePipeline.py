import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import TimeSeriesSplit
from sklearnUtilities.preprocessors import ColumnSelector
from sklearnUtilities.preprocessors import timeSeriesScaler
from sklearnUtilities.preprocessors import timeSeriesToFeatures 
from sklearnUtilities.preprocessors import createTimeFeatures 
from sklearnUtilities.preprocessors import TransformationWrapper
from sklearnUtilities.preprocessors import createTimeSeriesDiferences
from sklearnUtilities.preprocessors import FunctionTransformer

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
        0) Temporarily we are not going to fill empty values: I want the pipeline to break in that case to debug more thoroughly
        1) Bayes-encode the time features, maybe?
        2) How should the exogenous features feed this pipeline?
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