import pandas as pd #?
from datetime import datetime




# might want to keep many things preloaded

def modelSimulator(initialAmount, time, currentPosition):
	"""
		initialAmount = 1.0 typically
		times = [.. ,..., ..]
		positions = ['GS', 'MSFT', 'MSFT', 'MSFT', ]

		returns time series with the outcome of the stra
	"""
	assert len(time)==len(currentPosition), 'time and currentPosition must have the same size'
	outcome = [initialAmount]

	for t, pos in zip(time, currentPosition):
		increase = getIncrease(t, pos)
		outcome.append(outcome[-1]*increase)
	return outcome


def getIncrease(time, position):
	""" Returns the increase that we would get if we kept position at a certain time
	"""
	return 1.0