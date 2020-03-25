import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from scipy.stats import binom
from scipy.stats import beta
 


def getPrecisionRecallAlpha(y, scores, requiredPrecision):
	""" alphaProbability: the probability that the precision is bigger than requiredPrecision for each value of the threshold
		
		precisionRecallUtilities.py:16: FutureWarning: Indexing with multiple keys 
		(implicitly converted to a tuple of keys) will be deprecated, use a list instead.
  		dg = df.groupby('scores')['y', 'counter'].sum().sort_index(ascending=False).cumsum()
	"""
	df = pd.DataFrame({'y':y, 'scores': scores})
	df['counter']=1
	df.y= df.y.apply(int)
	dg = df.groupby('scores')[['y', 'counter']].sum().sort_index(ascending=False).cumsum()
	dg.columns = ['k', 'N']
	dg['precision']=dg.k/dg.N
	dg['recall']=dg.k/dg.k.max()
	dg['alphaProbability']=dg.apply(lambda x: 1-beta.cdf(requiredPrecision, 1+x.k, 1+x.N-x.k), axis=1)
	return dg.precision.values, dg.recall.values, dg.index.values, dg.alphaProbability.values


def getPrecisionRecall(y, scores, requiredPrecision):
	""" maybe not even using this. Not used (?)
	"""
	precision, recall, threshold, _ = getPrecisionRecallAlpha(y, scores, requiredPrecision)
	return precision, recall, threshold


def averageAlpha(ytrue, yScores, requiredPrecision):
	""" To be implemented. Not used (?)
	"""
	_, _, _, alpha = getPrecisionRecallAlpha(ytrue, yScores, requiredPrecision)
	return np.mean(alpha)


def selectThreshold(y, scores, requiredPrecision, requiredRecall, requiredCertainty):
	""" This is a key part of the code
		Maybe, this does not belong here.
	"""
	precision, recall, threshold, alpha = getPrecisionRecallAlpha(y, scores, requiredPrecision)
	I = [i for i in range(len(alpha)) if alpha[i]>=requiredCertainty]

	if len(I)==0: 
		return None, None, None, None

	index = max(I)
	if recall[index]<requiredRecall:
		return None, None, None, None

	return precision[index], recall[index], threshold[index], alpha[index]