
from datetime import datetime
from modeling.stockModel import stockModel

class moneyManager():
	""" Keeps only one position at the time !!!
	"""
	def __init__(self, stocks):
		self.stocks= stocks
		self.models = {s: stockModel(s) for s in stocks}
		self.currentTime = None # this is key!

	def updateTime(newTime):
		""" Piece of code tha needs to run every minute, maybe change the time
		"""
		self.currentTime = newTime
		for s in self.stocks:


