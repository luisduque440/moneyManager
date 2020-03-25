
from datetime import datetime
import pandas as pd
from stockModel.stockModel import stockModel
from sklearnUtilities.precisionRecallUtilities import selectThreshold
from stockModel.createTrainingDataSet import createTrainingDataSet

class moneyManager():
	""" * Keeps only one position at the time !!!
		* This class creates the multiple StockModels we need and runs them minute by minute
		* Uses the market simulator to see if we are performing good enough.
	"""
	def __init__(self, stocks, pastStarts=20, futureEnds=-20, trainSize=1200, 
		testSize=120, requiredPrecision=0.55, requiredRecall=0.05, requiredCertainty=0.9):
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

	def updateTime(self, currentTime):
		""" Piece of code tha needs to run every minute
		"""
		latestSuggestions = self.getLatestSuggestions(currentTime)
		self.suggestions += latestSuggestions
		self.updateThresholds(currentTime)
		self.updateLowPerformingModels(currentTime)

	def updateAllModels(self, currentTime):
		""" Document asap
		""" 
		for s in self.models: 
			self.updateModel(s, currentTime)

	def updateModel(self, stock, currentTime):
		""" Document asap
		"""
		print(stock)
		self.models[stock].train(currentTime)
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
		expected = createTrainingDataSet(stock, len(recordedScores), currentTime, self.pastStarts, self.futureEnds).target
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

			output = self.models[s].evaluate(currentTime)
			self.testSets[s].append((currentTime, output))

			threshold = self.thresholds[s]
			thresholdedOutput = (threshold!=None and output>threshold) 
			suggestion = ('BUY', s, currentTime) if thresholdedOutput else ('NON', s, currentTime)
			latestSuggestions.append(suggestion)
		return latestSuggestions


	def updateLowPerformingModels(self, currentTime):
		""" document asap
		"""
		modelRequiresUpdate = lambda s: self.thresholds[s]==None and self.testSetIsBig(s)
		for s in self.stocks:
			if modelRequiresUpdate(s):
				self.updateModel(s, currentTime)
