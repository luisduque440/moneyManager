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
   
