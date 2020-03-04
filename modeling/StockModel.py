from sklearn.pipeline import Pipeline
from modeling.sklearnUtilities import ColumnSelector
from modeling.sklearnUtilities import timeSeriesScaler
from modeling.sklearnUtilities import timeSeriesToFeatures 
from modeling.sklearnUtilities import createTimeFeatures 
from modeling.sklearnUtilities import TransformationWrapper
from modeling.sklearnUtilities import BayesianCategoricalEncoder
from modeling.sklearnUtilities import bayesianTransformer
from modeling.sklearnUtilities import createTimeSeriesDiferences
from modeling.sklearnUtilities import FunctionTransformer
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

    """
    def __init__(self, stock, requiredTrainingSamples= 3000, requiredEvaluationSamples=200, 
                              requiredPrecision, requiredRecall, ):

        self.requiredTrainingSamples = requiredTrainingSamples
        self.requiredEvaluationSamples = requiredEvaluationSamples
        self.stock = stock
        self.model = None
        

    def getModelSuggestions(currentTime):
        self.gatherEvaluationSamples()
        if self.modelIsValid():
            threshold = 



    def modelIsValid(currentTime):
        print('many reasons model is not valid')

    def getModelThreshold():
        # really

    def fullyTrain(self):
        self.gatherData()
        return self


    def gatherData(self):
        df = pd.DataFrame()
        return df

    def getLatestOrderSuggestions(self):
        return 



def generatePipeline(levelDictionary=None):
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
        
        #('classifier', LogisticRegression(penalty='none', solver='sag', max_iter=1000))
    ])
    return pipeline


#X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
#pca = PCA(n_components=2)

# try pca asap !!

#('scaletimeseries', FunctionTransformer(timeSeriesScaler)),
#('bayesianencoder', BayesianCategoricalEncoder()),
#('bayesiantransformer', FunctionTransformer(bayesianTransformer, levelDictionary)),

