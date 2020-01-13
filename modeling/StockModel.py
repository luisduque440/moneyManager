from sklearn.pipeline import Pipeline
from modeling.sklearnUtilities import ColumnSelector
from modeling.sklearnUtilities import timeSeriesScaler
from modeling.sklearnUtilities import timeSeriesToFeatures 
from modeling.sklearnUtilities import createTimeFeatures 
from modeling.sklearnUtilities import TransformationWrapper
from modeling.sklearnUtilities import BayesianCategoricalEncoder
from modeling.sklearnUtilities import createTimeSeriesDiferences
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression



class stockModel():
    """Wrapper of a single pipeline with its respective thresholds, train datasets,  evaluators, performance
    """
    def __init__(self, stockSymbol, startDay, endDay):
        self.stockSymbol = stockSymbol
        self.startDay = startDay
        self.endDay = endDay
        self.validModel = None
        self.pipelineInfo = {}
        self.percentageOfDataSetAvailable = None
    
    def fullyTrain(self):
        self.gatherData()
        return self


    def gatherData(self):
        df = pd.DataFrame()
        return df

    def getLatestOrderSuggestions(self):
        return 



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
        #('scaletimeseries', FunctionTransformer(timeSeriesScaler)),
        ('createdifferences', FunctionTransformer(createTimeSeriesDiferences)), 
        ('timeSeriesToFeatures', FunctionTransformer(timeSeriesToFeatures)), 
        ('createtimefeatures', FunctionTransformer(createTimeFeatures)),
        ('bayesianencoder', BayesianCategoricalEncoder()),
        ('scaler', TransformationWrapper(MinMaxScaler())),
        ('classifier', LogisticRegression(penalty='none', solver='sag', max_iter=1000))
    ])
    return pipeline
