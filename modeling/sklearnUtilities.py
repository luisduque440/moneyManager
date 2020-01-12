import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin



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
    

def featureEngineering(df):
    """ Start documenting this
    """
    colnames = df.columns
    listTransforms = {'max': max, 'argmax':np.argmax, 'min': min, 'argmin':np.argmin, 'mean':np.mean, 'std': np.std, 'median': np.median, 'last': lambda x:x[-1]}
    listToStats = lambda x: [listTransforms[trf](x) for trf in listTransforms]
    statsNames = list(listTransforms.keys())

    timeTransforms = {'hour': (lambda x: x.hour), 'tenminute': (lambda x: x.minute//10)}
    timeToStats = lambda x: [timeTransforms[trf](x) for trf in timeTransforms]
    timeFeatureNames = list(timeTransforms.keys())

    for col in colnames: 
        df[col] = df[col].apply(listToStats)

    df['dateTime'] = df.index.map(timeToStats)
    df = df.apply(lambda x: pd.Series(sum(x.values, [])), axis=1)

    featureNames = []
    for col in colnames:
        featureNames = featureNames + [str(col)+'_'+str(stat) for stat in statsNames]
    df.columns = (featureNames + timeFeatureNames)
    return df


def timeSeriesScaler(df):
    """ Start documenting this
    """
    #df['currentValue'] = df.Close.apply(lambda x: x[-1])
    #df['currentVolume'] = df.Volume.apply(lambda x: x[-1])
    #df['Volume']=df.apply(lambda x: np.array(x['Volume'])/x.currentVolume, axis=1)
    #for col in ['Open', 'High', 'Low', 'Close']:
    #    df[col]=df.apply(lambda x: np.array(x[col])/x.currentValue, axis=1)
    #return df.drop(columns = ['currentValue', 'currentVolume'])
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

        if self.colsToEncode ==None:
            self.categorical_columns = list(df.columns)
        else:
            self.categorical_columns = self.colsToEncode

        self.level_dictionary={}
        df['target']=y
        for col in self.categorical_columns:
            importance = df.groupby(col)['target'].agg([np.sum, np.size])
            self.level_dictionary[col] = 1.0*importance['sum']/(importance['size']) 
        return self
    
    def transform(self, X):
        df=pd.DataFrame(index=X.index)
        dictionary = self.level_dictionary
        for col in self.categorical_columns:
            df[col] = X[col].apply(lambda x: dictionary[col][x] if x in dictionary[col].index else None)
        return df




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
   
