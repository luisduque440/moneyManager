from sklearn.pipeline import Pipeline
from modeling.transformations import ColumnSelector
from modeling.transformations import timeSeriesScaler
from modeling.transformations import featureEngineering
from modeling.transformations import TransformationWrapper
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression



def generatePipeline():
    """ start documenting this 
    To do:
    	0) The name of this should change: generateTimeSeriesPipeline()
        1) classifier could be a parameter, columns to use could be parameters
        2) Include differences as features too.
        3) Bayes-encode the time features
        4) How should the exogenous features feed this pipeline?
    """
	pipeline = Pipeline([
	    ('selectcolumns', ColumnSelector(columns = ['Open', 'High', 'Low', 'Close', 'Volume'])), 
	    ('scaletimeseries', FunctionTransformer(timeSeriesScaler)),
	    ('featurengineering', FunctionTransformer(featureEngineering)),
	    # more feature engineering: bayesianEncoder for time, pca, log transformations, blah blah.
	    ('scaler', TransformationWrapper(MinMaxScaler())), ## the columns are lost :( put my own.
	    ('classifier', LogisticRegression(penalty='none', solver='sag', max_iter=1000)) # consider : LogisticRegressionCV
	])
	return pipeline
