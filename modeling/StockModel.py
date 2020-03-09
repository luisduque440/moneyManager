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
from modeling.precisionRecallUtilities import selectThreshold
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
    				   requiredPrecision=0.55, requiredRecall=0.5, requiredCertainty=0.9):

        self.stock = stock
        self.requiredTrainingSamples = requiredTrainingSamples
        self.requiredEvaluationSamples = requiredEvaluationSamples
        self.requiredPrecision = requiredPrecision 
        self.requiredRecall = requiredRecall 
        self.requiredCertainty = requiredCertainty
        self.model = None


    def getModelSuggestion(self, currentTime):
    	self.currentTime = currentTime
    	order=self.generateNullOrder()
        if self.modelIsValid() and self.thresholdedOutput():
  			order = self.generateBuyOrder()
     	else:
     		self.train()
     	return order 
  			

  	def train(self):
  		""" 
  		"""
        self.getTrainDataSets()
        self.getEvaluationDataSet()

		classifiers = [NaiveBayes(), logisticRegression(), ridge(), lasso()]
        for clf in classifiers:
        	self.model = generatePipeline(clf)
        	self.model.fit(self.Xtrain, self.ytrain)
        	_,_, self.threshold, _ = selectThreshold(y, scores, requiredPrecision, requiredRecall, requiredCertainty)
        	if self.modelIsValid():
        		break
		
    def modelIsValid(self):
		if self.threshold==None or self.modelHasNotBeenTrainedInAWhile(): 
			return False
		return True

    def getModelThreshold(self):
        # really
        return 


    def thresholdedOutput(self):
    	return 

    def modelHasNotBeenTrainedInAWhile(self):
    	return

    def getTrainDataSets(self):
        df = pd.DataFrame()
        return df

    def getEvaluationDataSet(self):
        df = pd.DataFrame()
        return df


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
        
    ])
    return pipeline





	def generateBuyOrder(self):
		buyOrder =  {'orderType': 'BUY', 
				'stock': self.stock,  
				'generatedAt': datetime.now(), 
				'expiresAt': datetime(2040,1,1)
				'precision': 0.666,
				'recall': 0.222}
		return buyOrder


	def generateNullOrder(self):
		buyOrder =  {'orderType': 'NULL', 
				'stock': self.stock,  
				'generatedAt': datetime.now(), 
				'expiresAt': datetime(2040,1,1)
				'precision': 0.666,
				'recall': 0.222}
		return buyOrder

#X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
#pca = PCA(n_components=2)
#('scaletimeseries', FunctionTransformer(timeSeriesScaler)),


