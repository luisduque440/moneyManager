from sklearn.pipeline import Pipeline
from modeling.transformations import ColumnSelector
from modeling.transformations import timeSeriesScaler
from modeling.transformations import featureEngineering
from modeling.transformations import TransformationWrapper
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import MinMaxScaler



def generatePipeline():
	pipeline = Pipeline([
	    ('selectcolumns', ColumnSelector(columns = ['Open', 'High', 'Low', 'Close', 'Volume'])), 
	    ('scaletimeseries', FunctionTransformer(timeSeriesScaler)),
	    ('featurengineering', FunctionTransformer(featureEngineering)),
	    # more feature engineering: bayesianEncoder for time, pca, log transformations, blah blah.
	    ('scaler', TransformationWrapper(MinMaxScaler())) ## the columns are lost :( put my own.
	    #('classifier', SVC()), # consider : LogisticRegressionCV
	])
	return pipeline
