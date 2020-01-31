import pandas as pd 
from datetime import datetime
from .loadTimeSeries import loadIncreaseTimeSeries

stockSeriesIncreases = loadIncreaseTimeSeries()

# bad name bot for the function and for the file
def marketSimulator(positionTS, initialAmount=1.0):
	"""
		positionTimeSeries: a pd.Series indexed with times having the name of the asset that is held minute by minute
		initialAmount: amount of cash that we have at the beginning
		returns: time series with the money if we held the assets specified on positionTS
	"""
	positionDF= positionTS.reset_index().copy()
	positionDF.columns = ['date', 'position']
	positionIncreases = positionDF.apply(lambda x: stockSeriesIncreases[x.position][x.date], axis=1)
	positionIncreases.index= positionTS.index
	positionIncreases.values[0]=initialAmount
	positionValue = positionIncreases.cumprod()
	return positionValue



# Use the following in test_marketSimulator.py
#from .loadTimeSeries import loadTimeSeries
#def testCaseForModelSimulator():
	#S=loadTimeSeries('GS', datetime(2019,1,1), datetime(2020,1,1)).consolidated
	#positionTS=pd.Series(['GS']*len(S),index=S.index)
	#win = modelSimulator(positionTS, initialAmount=S.values[0])
	# S and win must be *almost* the same