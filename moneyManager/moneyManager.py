
from datetime import datetime
from stockModel.stockModel import stockModel

class moneyManager():
	""" * Keeps only one position at the time !!!
		* This class creates the multiple StockModels we need and runs them minute by minute
		* Uses the market simulator to see if we are performing good enough.
	"""
	def __init__(self, stocks, testSize, requiredPrecision, requiredRecall, requiredCertainty):
		""" Document asap
		"""
		self.stocks = stocks
		self.testSize = testSize
		self.requiredPrecision = requiredPrecision
		self.requiredRecall = requiredRecall
		self.requiredCertainty = requiredCertainty
		self.models = {s: stockModel(s) for s in stocks}
		self.threholds = {s: None for s in stocks}
		self.previousScores = {s: [] for s in stocks}
		self.suggestions = [] 

	def updateTime(currentTime):
		""" Piece of code tha needs to run every minute, maybe change the time
		"""
		self.updateThresholds(currentTime)
		latestSuggestions = self.getLatestSuggestions(currentTime)
		self.suggestions += latestSuggestions
		self.updateLowPerformingModels(currentTime):

	def updateAllModels(self, currentTime):
		""" Document asap
		""" 
		for s in self.models: 
			self.updateModel(s, currentTime)

	def updateModel(self, stock, currentTime):
		""" Document asap
		"""
		self.models[s].train(currentTime)
		self.previousScores[s]=[]

	def updateThresholds(self, currentTime):
		""" Document asap
		"""
		testSetIsBigEnough = lambda s: len(self.previousScores[s])>=self.testSize	
		self.thresholds={s : self.getThreshold(s) if testSetIsBigEnough(s) else None for s in self.stocks}

	def getThreshold(self, stock):
		""" Document asap. NEEDS WORK.
		"""
		expectedOutcome=None #need to get this.
		scores=None # need to get this.
		p,r,threshold,a = selectThreshold(expectedOutcome, scores, self.requiredPrecision, self.requiredRecall, self.requiredCertainty)
		return threshold


	def getLatestSuggestions(self, currentTime):
		""" Document asap
		"""
		latestSuggestions = []
		for s in self.stocks:
			output = self.models[s].evaluate(currentTime)
			self.previousScores[s].append((currentTime, modelOutput))
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
