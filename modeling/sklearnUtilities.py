import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


timeToStatsDict = {
    'hour': (lambda x: 'hour='+str(x.hour)), 
    'minute': (lambda x: 'minute='+str(x.minute)), 
    'hourminute': (lambda x: str(x.minute)+':'+str(x.hour)) 
}


listToStatsDict = {
    'max': max, 'argmax':np.argmax, 'min': min, 'argmin':np.argmin, 
    'mean':np.mean, 'std': np.std, 'median': np.median, 'last': lambda x:x[-1]
}


class ColumnSelector(BaseEstimator, TransformerMixin):
    """Used to explicitly select the columns in a pipeline
    """
    
    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        for c in self.columns: assert c in list(X.columns), "the data frame is missing column %s" %(c)
        df = X[self.columns].copy()
        return df



def createTimeFeatures(df, timeToStatsDict=timeToStatsDict):
    """ Creates minute of the day, 
    """
    timeToStats = lambda x: [timeToStatsDict[trf](x) for trf in timeToStatsDict]
    timeFeatureNames = list(timeToStatsDict.keys())
    dT = pd.DataFrame(index=df.index)
    dT['datetime'] = df.index.map(timeToStats)
    dT = dT.apply(lambda x: pd.Series(sum(x.values, [])), axis=1)
    dT.columns = timeFeatureNames
    df = df.merge(dT, how='left', left_index=True, right_index=True)
    return df


def timeSeriesToFeatures(df, listToStatsDict = listToStatsDict):
    """ Start documenting this
    """
    originalColnames = list(df.columns)
    listToStats = lambda x: [listToStatsDict[trf](x) for trf in listToStatsDict]
    for col in df.columns: 
        df[col] = df[col].apply(listToStats)

    df = df.apply(lambda x: pd.Series(sum(x.values, [])), axis=1)

    featureNames = []
    statsNames = list(listToStatsDict.keys())
    for col in originalColnames:
        featureNames = featureNames + [str(col)+'_'+str(stat) for stat in statsNames]
    df.columns = featureNames
    return df

def createTimeSeriesDiferences(df): # should we also add cumulative sums (??)
    """ Start documenting this
    """
    for col in df.columns:
        df[col+'Difference']= df[col].apply(lambda x: [x[i]-x[i-1] for i in range(1,len(x))])
    return df



def timeSeriesScaler(df):
    """ Start documenting this
    """
    dg = pd.DataFrame(index=df.index)
    for col in df.columns: 
        dg[col]=df[col].apply(lambda x: list(np.array(x)/x[-1]))
    return dg


class BayesianCategoricalEncoder(TransformerMixin):  
    """Label encodes all the columns of a dataframe.
 
    Args:
        df
        
    Returns:
        DataFrame with object dtypes label-encoded. Notice that this is not just a
        typical Label Encoder. For each categorical column in the data frame, the levels
        are encoded proporcional to how much transaction revenue they generate. 
        
        For example, as 
        (avg spent in USA) > (avg spent in Great Britain) > (avg spent spent in Argentina)
        the encoded labels of USA, Great Britain and Argentina are expected to preserve 
        the same order
 
    Notes:
        BayesianCategoricalEncoder is a bad name for this class. Apparently this type of encoders has a name
        potential improvement: add an option that creates another column with the 'support' of the quotient.
    """
    def __init__(self, colsToEncode=None):
        self.colsToEncode = colsToEncode

    def fit(self, X, y):
        df = X.select_dtypes(include='object').copy()
        self.catCols = list(df.columns) if self.colsToEncode==None else self.colsToEncode
        self.levelDictionary={}
        df['target']=y
        for col in self.catCols:
            importance = df.groupby(col)['target'].agg([np.sum, np.size])
            self.levelDictionary[col] = 1.0*importance['sum']/(importance['size']) 
        return self
    
    def transform(self, X):
        dictionary = self.levelDictionary
        for col in self.catCols:
            X[col] = X[col].apply(lambda x: dictionary[col][x] if x in dictionary[col].index else None)
        return X


class TransformationWrapper(BaseEstimator, TransformerMixin):
	"""Scaler wrapper to have pandas compatibility.

	Example
	    >> dg = pd.DataFrame({'A':[0.5, 0.6, 0.7]})
	    >> NumericFeaturesScaler(transformation = MinMaxScaler()).fit(dg).transform(dg)
	    0  0.0
	    1  0.5
	    2  1.0

	Attributes:
	    transformation: a sklearn transformation, typically a scaler
	"""
	def __init__(self, transformation):
		self.transformation = transformation

	def fit(self, X, y=None):
		self.transformation.fit(X)
		return self

	def transform(self, X):
		return pd.DataFrame(self.transformation.transform(X), columns = X.columns, index=X.index)


class sampleTransformer(BaseEstimator, TransformerMixin):
    """sample way of building things
    """
    def __init__(self, parameter=None):
        pass
    
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        df=X.copy()
        return df
   
