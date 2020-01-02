import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin



class ColumnSelector(BaseEstimator, TransformerMixin):
    """Transformation used to explicitly learn or select the columns from a data frame.
    The columns could be explicitly selected or learnt from another data frame
    """
    
    def __init__(self, columns=None):
        self.columns = columns
    
    def fit(self, X, y=None):
        if self.columns==None: self.columns = list(X.columns)
        return self
        
    def transform(self, X):
        for c in self.columns: assert c in list(X.columns), "the data frame is missing column %s" %(c)
        df = X[self.columns].copy()
        return df
    
    
def featureEngineering(df):
    """ better do this:
    https://scikit-learn.org/stable/auto_examples/preprocessing/plot_function_transformer.html#sphx-glr-auto-examples-preprocessing-plot-function-transformer-py
    """
    listToStats = lambda x: [max(x), min(x), np.mean(x), np.std(x), np.median(x)]
    statsNames = ['max', 'min', 'mean', 'std', 'median']
    for col in df.columns: 
        df[col] = df[col].apply(listToStats)
    timeToFeatures = lambda x: [45, 69] # these could even be categorical.
    df['dateTime'] = df.index.map(timeToFeatures)
    df = df.apply(lambda x: pd.Series(sum(x.values, [])), axis=1)

    newColnames = []
    for col in df.columns:
        newColnames = newColnames + [str(col)+str(stat) for stat in statsNames]

    df.columns = list(newColnames)

    #df.columns = ['feat_%s'%(i) for i in range(df.shape[1])]
    return df


def timeSeriesScaler(df):
    """ better do this:
    https://scikit-learn.org/stable/auto_examples/preprocessing/plot_function_transformer.html#sphx-glr-auto-examples-preprocessing-plot-function-transformer-py
    """
    df['currentValue'] = df.Close.apply(lambda x: x[-1])
    df['currentVolume'] = df.Volume.apply(lambda x: x[-1])
    df['Volume']=df.apply(lambda x: np.array(x['Volume'])/x.currentVolume, axis=1)
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col]=df.apply(lambda x: np.array(x[col])/x.currentValue, axis=1)
    return df.drop(columns = ['currentValue', 'currentVolume'])





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
   
