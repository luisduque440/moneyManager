import pandas as pd 
from datetime import datetime
from loadTimeSeries import loadAvailableIncreaseTimeSeries

stockSeriesDic = loadAvailableIncreaseTimeSeries(datetime(2019,1,1), datetime(2020,1,1))

def modelSimulator(initialAmount, positionTS):
	"""
		positionTimeSeries = a pd.Series indexed with times
		returns time series with the outcome of the stra
	"""
	positionDF= positionTS.reset_index()
	positionDF.columns = ['date', 'position']
	positionIncreases = positionDF.apply(lambda x: stockSeriesDic[x.position][x.date], axis=1)
	return positionIncreases

# so elegant  and concise.