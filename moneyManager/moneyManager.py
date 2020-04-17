import pandas as pd
from stockModel.stockModel import stockModel
from sklearnUtilities.precisionRecallUtilities import selectThreshold
from stockModel.createTrainingDataSet import createTarget, _keepRowsWithIndexesInBoth
class moneyManager():
	"""
		* Creates multiple stockModels and updates them minute by minute.
		* StockModels return a score every minute
		* The method updateThresholds decides if there is a threshold that makes the StockModel reliable
		* If there is a valid threshold
	"""
	def __init__(self, stocks, pastLen=20, futureLen=20, trainSize=1200,
		testSize=120, requiredPrecision=0.50, requiredRecall=0.05, requiredCertainty=0.85):
		""" Document asap
		"""
		self.stocks = stocks
		self.pastLen = pastLen
		self.futureLen = futureLen
		self.trainSize = trainSize
		self.testSize = testSize
		self.requiredPrecision = requiredPrecision
		self.requiredRecall = requiredRecall
		self.requiredCertainty = requiredCertainty
		self.models = {s: stockModel(s, pastLen, futureLen, trainSize) for s in stocks}
		self.thresholds = {s: None for s in stocks}
		self.testSets = {pd.Series(): [] for s in stocks}
		self.suggestions = [] 

	def update(self, currentTime):
		""" Piece of code tha needs to run every minute
		"""
		self.suggestions += self.getLatestSuggestions(currentTime)
		self.updateThresholds(currentTime)
		self.updateLowPerformingModels(currentTime)

	def updateAllModels(self, currentTime):
		""" Document asap
		""" 
		for s in self.models: 
			self.updateSingleModel(s, currentTime)

	def updateSingleModel(self, stock, currentTime):
		""" Document asap
		"""
		print('training model for ', stock)
		self.models[stock].fit(currentTime)
		self.testSets[stock]=pd.Series()

	def updateThresholds(self, currentTime):
		""" Document asap
		"""
		self.thresholds={s : self.getThreshold(s, currentTime) if self.testSetIsBig(s) else None for s in self.stocks}

	def testSetIsBig(self, s):
		return len(self.testSets[s])>=self.testSize

	def getThreshold(self, stock, currentTime):
		""" Document asap. NEEDS WORK, very careful on how scores, and expected are merged.
		"""
		precision, recall, certainty = self.requiredPrecision, self.requiredRecall, self.requiredCertainty
		expected=createTarget(stock, len(recordedScores), currentTime, self.futureLen)
		scores = self.testSets[stock]
		expected, scores= _keepRowsWithIndexesInBoth(expected, scores)
		_,_,threshold,_ = selectThreshold(expected, scores, precision, recall, certainty)
		return threshold


	def getLatestSuggestions(self, currentTime):
		""" Document asap
		"""
		latestSuggestions = []
		for s in self.stocks:
			if self.testSetIsBig(s): self.testSets[s]=self.testSets[s][1:]
			output = self.models[s].predict_proba(currentTime)
			self.testSets[s] = self.testSets[s].append(pd.Series([output], index=[currentTime])))
			threshold = self.thresholds[s]
			thresholdedOutput = (threshold!=None and output>threshold)
			suggestion = ('buyAndKeep20mins', s, currentTime) if thresholdedOutput else ('none', s, currentTime)
			latestSuggestions.append(suggestion)
		return latestSuggestions


	def updateLowPerformingModels(self, currentTime):
		""" document asap
		"""
		modelRequiresUpdate = lambda s: self.thresholds[s]==None and self.testSetIsBig(s)
		for s in self.stocks:
			if modelRequiresUpdate(s):
				self.updateSingleModel(s, currentTime)