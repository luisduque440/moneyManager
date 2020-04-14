
from datetime import datetime
import pandas as pd
from stockModel.stockModel import stockModel
from sklearnUtilities.precisionRecallUtilities import selectThreshold
from stockModel.createTrainingDataSet import createTarget

class moneyManager():
	"""
		* Creates multiple stockModels and updates them minute by minute.
		* StockModels return a score every minute
		* The method updateThresholds decides if there is a threshold that makes the StockModel reliable
		* If there is a valid threshold
	"""
	def __init__(self, stocks, pastStarts=20, futureEnds=-20, trainSize=1200, 
		testSize=120, requiredPrecision=0.50, requiredRecall=0.05, requiredCertainty=0.9):
		""" Document asap
		"""
		self.stocks = stocks
		self.pastStarts = pastStarts
		self.futureEnds = futureEnds
		self.trainSize = trainSize
		self.testSize = testSize
		self.requiredPrecision = requiredPrecision
		self.requiredRecall = requiredRecall
		self.requiredCertainty = requiredCertainty
		self.models = {s: stockModel(s, pastStarts, futureEnds, trainSize) for s in stocks}
		self.thresholds = {s: None for s in stocks}
		self.testSets = {s: [] for s in stocks}
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
		self.testSets[stock]=[]

	def updateThresholds(self, currentTime):
		""" Document asap
		"""
		self.thresholds={s : self.getThreshold(s, currentTime) if self.testSetIsBig(s) else None for s in self.stocks}

	def testSetIsBig(self, s):
		return len(self.testSets[s])>=self.testSize

	def getThreshold(self, stock, currentTime):
		""" Document asap. NEEDS WORK, very careful on how scores, and expected are merged.
		"""
		recordedScores = self.testSets[stock]
		scores = pd.Series([r[1] for r in recordedScores], index=[r[0] for r in recordedScores])
		expected = createTarget(stock, len(recordedScores), currentTime, self.futureEnds)
		dg = pd.concat([scores, expected], axis=1, join='inner').dropna()
		dg.columns = ['scores', 'expected']
		self.dg = dg.copy() # for debugging
		p,r,threshold,a = selectThreshold(dg.expected, dg.scores, self.requiredPrecision, self.requiredRecall, self.requiredCertainty)
		return threshold

	def getLatestSuggestions(self, currentTime):
		""" Document asap
		"""
		latestSuggestions = []
		for s in self.stocks:
			if self.testSetIsBig(s):
				self.testSets[s].pop(0)

			output = self.models[s].predict_proba(currentTime)
			self.testSets[s].append((currentTime, output))

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


	def evaluateAvailableSuggestions(self):
		# check how many of our suggestions were actually correct:
		buySuggestions = self._getBuySuggestions()
		idealBuyTimes = self._getIdealBuyTimes()
		correctBuySuggestions = {}
		for s in stocks:
			correctBuySuggestions[s] = [b for b in buySuggestions[s] if b in idealBuyTimes[s]]

		buySuggestionsCount = sum([len(buySuggestions[s]) for s in stocks])
		print(buySuggestionsCount)
		correctBuySuggestionsCount = sum([len(correctBuySuggestions[s]) for s in stocks])
		print(correctBuySuggestionsCount)

	def _getBuySuggestions(self):
		""" document
		"""
		managerSuggestions = [b for b in self.suggestions if b[0] == 'buyAndKeep20mins']
		buySuggestions = {}
		for s in self.stocks:
			buySuggestions[s] = {b[2] for b in managerSuggestions if b[1] == s}
		return buySuggestions

	def _getIdealBuyTimes(self):
		""" gets Times in which it is a good idea to buyAndKeep for 20 mins
		"""
		idealBuyTimes = {}
		for s in self.stocks:
			ds = loadTimeSeries(s)
			dB = createTarget(ds)
			idealBuyTimes[s] = set(dB[dB == True].index)
		return idealBuyTimes







