
from datetime import datetime
import pandas as pd
from stockModel.stockModel import stockModel
from sklearnUtilities.precisionRecallUtilities import selectThreshold


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
		self.threholds = {s: None for s in stocks}
		self.previousScores = {s: [] for s in stocks}
		self.suggestions = [] 

	def updateTime(currentTime):
		""" Piece of code tha needs to run every minute, maybe change the time
		"""
		self.updateThresholds(currentTime)
		latestSuggestions = self.getLatestSuggestions(currentTime)
		self.suggestions += latestSuggestions
		self.updateLowPerformingModels(currentTime)

	def updateAllModels(self, currentTime):
		""" Document asap
		""" 
		for s in self.models: 
			self.updateModel(s, currentTime)

	def updateModel(self, stock, currentTime):
		""" Document asap
		"""
		self.models[stock].train(currentTime)
		self.previousScores[stock]=[]

	def updateThresholds(self, currentTime):
		""" Document asap
		"""
		testSetIsBigEnough = lambda s: len(self.previousScores[s])>=self.testSize	
		self.thresholds={s : self.getThreshold(s, currentTime) if testSetIsBigEnough(s) else None for s in self.stocks}

	def getThreshold(self, stock, currentTime):
		""" Document asap. NEEDS WORK.
		"""
		recordedScores = self.previousScores[s]
		scores = pd.Series([r[1] for r in recordedScores], index=[r[0] for r in recordedScores])
		expected = createTrainingDataSet(self.stock, len(recordedScores), currentTime, self.pastStarts, self.futureEnds).target
		df = pd.concat([scores, expected]).dropna()
		df.columns = ['scores', 'expected']
		p,r,threshold,a = selectThreshold(df.expected, df.scores, self.requiredPrecision, self.requiredRecall, self.requiredCertainty)
		return threshold

	def getLatestSuggestions(self, currentTime):
		""" Document asap
		"""
		latestSuggestions = []
		for s in self.stocks:
			output = self.models[s].evaluate(currentTime)
			self.previousScores[s].append((currentTime, modelOutput))

			if len(self.previousScores[s])>self.testSize:
				self.previousScores[s].pop(0)

			thresholdedOutput = (threshold!=None and output>threshold) 
			suggestion = ('BUY', s, currentTime) if thresholdedOutput else ('NON', s, currentTime)
			latestSuggestions.append(suggestion)
		return latestSuggestions


	def updateLowPerformingModels(self, currentTime):
		""" document asap
		"""
		modelRequiresUpdate = lambda s: self.thresholds[s]==None and len(self.modelOutputs[s])>=self.testSize
		for s in self.stocks:
			if modelRequiresUpdate(s):
				self.updateModel(s, currentTime)
