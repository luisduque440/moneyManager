import pandas as pd
import numpy as np


error_msg_column_list_is_not_valid = "the list of columns has repeated elements"
error_msg_column_not_found = 'the data frame is missing column %s'


class ColumnSelector(BaseEstimator, TransformerMixin):
    """Transformation used to explicitly learn or select the columns from a data frame.
    The columns could be explicitly selected or they could be learnt from another data frame
    as in the following examples
    
    Example 1
        >> from pipeline_utilities import ColumnSelector
        >> df = pd.DataFrame({'A':['May', 'August', 'Jun'],'B':[4, 3, 4],'C':[5.0, 8.0, 1.0]})
        >> ColumnSelector(columns= ['A', 'C']).transform(df)
        0  May      5.0
        1  August   8.0
        2  Jun      1.0
        
        
        
    Example 2
        >> from pipeline_utilities import ColumnSelector
        >> df = pd.DataFrame({'A':['House', 'Star'], 'C':[1.0, 2.0, 1.0]})
        >> dg = pd.DataFrame({'A':['May', 'August', 'Jun'],'B':[4, 3, 4],'C':[5.0, 8.0, 1.0]})
        >> ColumnSelector().fit(df).transform(dg)
        0  May      5.0
        1  August   8.0
        2  Jun      1.0
    """
    
    def __init__(self, columns=None):
        self.columns = columns
    
    def fit(self, X, y=None):
        if self.columns==None: self.columns = list(X.columns)
        assert len(self.columns)==len(set(self.columns)), error_msg_column_list_is_not_valid
        return self
        
    def transform(self, X):
        if len(self.columns)==0: return pd.DataFrame()
        for c in self.columns: assert c in list(X.columns), error_msg_column_not_found %(c)
        df = X[self.columns].copy()
        return df
    
    
def featureEngineering(dg):
'''  
better do this:
https://scikit-learn.org/stable/auto_examples/preprocessing/plot_function_transformer.html#sphx-glr-auto-examples-preprocessing-plot-function-transformer-py
'''
    df = dg.copy()
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    listToStats = lambda x: [max(x), min(x), np.mean(x), np.std(x), np.median(x)]
    timeToFeatures = lambda x: [1,2,3,4,5,6,7] # these could even be categorical.

    for col in columns:
        df[col] = df[col].apply(listToStats)
    
    df['dateTime'] = df.index.map(timeToFeatures)
    return df


def myScaler(dg):
'''  
better do this:
https://scikit-learn.org/stable/auto_examples/preprocessing/plot_function_transformer.html#sphx-glr-auto-examples-preprocessing-plot-function-transformer-py
'''
    df = dg.copy()
    df['currentValue'] = df.Close.apply(lambda x: x[-1])
    df['currentVolume'] = df.Volume.apply(lambda x: x[-1])
    dg['Volume']=dg.apply(lambda x: np.array(x['Volume'])/x.currentVolume, axis=1)
    for col in ['Open', 'High', 'Low', 'Close']:
        dg[col]=dg.apply(lambda x: np.array(x[col])/x.currentValue, axis=1)

    df = dg.apply(lambda x: np.array(x.pastLow)/x.currentValue, axis=1)
    df = df.drop(columns = ['currentValue', 'currentVolume'])
    return df





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
   
