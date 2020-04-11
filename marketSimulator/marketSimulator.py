from loadData.loadTimeSeries import loadIncreaseTimeSeries

stockSeriesIncreases = loadIncreaseTimeSeries()

def getIncreasesTS(positionTS, initialAmount=1.0):
	positionDF= positionTS.reset_index().copy()
	positionDF.columns = ['date', 'position']
	increases = positionDF.apply(lambda x: stockSeriesIncreases[x.position][x.date], axis=1)
	increases.index= positionTS.index
	increases.values[0]=initialAmount
	return increases

def marketSimulator(positionTS, initialAmount=1.0):
	"""
		positionTimeSeries: a pd.Series indexed with times having the name of the asset that is held minute by minute
		initialAmount: amount of cash that we have at the beginning
		returns: time series with the money if we held the assets specified on positionTS
	"""
	increases = getIncreasesTS(positionTS, initialAmount)
	positionValue = increases.cumprod()
	return positionValue


def getPercentageOfIncreases(positionTS, initialAmount=1.0):
	""" This has never been tested
	"""
	increases = getIncreasesTS(positionTS, initialAmount)
	positiveIncreases = (increases>1.0).sum()
	return 1.0*positiveIncreases/len(increases)





