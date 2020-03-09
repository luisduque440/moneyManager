import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
from scipy.stats import beta
from sklearn.metrics import average_precision_score


def getPrecisionRecallAlpha(y, scores, requiredPrecision):
	""" alphaProbability: the probability that the precision is bigger than requiredPrecision for each value of the threshold
	"""
	df = pd.DataFrame({'y':y, 'scores': scores})
	df['counter']=1
	df.y= df.y.apply(int)
	dg = df.groupby('scores')['y', 'counter'].sum().sort_index(ascending=False).cumsum()
	dg.columns = ['k', 'N']
	dg['precision']=dg.k/dg.N
	dg['recall']=dg.k/dg.k.max()
	dg['alphaProbability']=dg.apply(lambda x: 1-beta.cdf(requiredPrecision, 1+x.k, 1+x.N-x.k), axis=1)
	return dg.precision.values, dg.recall.values, dg.index.values, dg.alphaProbability.values


def getPrecisionRecall(y, scores, requiredPrecision):
	""" maybe not even using this
	"""
	precision, recall, threshold, _ = getPrecisionRecallAlpha(y, scores, requiredPrecision)
	return precision, recall, threshold


def averageAlpha(ytrue, yScores, requiredPrecision):
	""" To be implemented
	"""
	_, _, _, alpha = getPrecisionRecallAlpha(ytrue, yScores, requiredPrecision)
	return np.mean(alpha)


##   careful, the order of these parameters changed, requiredRecall not implemented
##  The following function MUST be refactored to ONLY return the threshold?
def selectThreshold(y, scores, requiredPrecision, requiredRecall, requiredCertainty):
	"""
		returns 
	"""
	precision, recall, threshold, alpha = getPrecisionRecallAlpha(y, scores, requiredPrecision)
	I = [i for i in range(len(alpha)) if alpha[i]>=requiredCertainty]
	if len(I)>0:
		index = max(I)
		return precision[index], recall[index], threshold[index], alpha[index]

	else:
		return None,None,None,None



def getNpvTnrThreshold(ytrue, ypredicted):
	""" To be implemented
	"""
	pass




def getProbabilityNpvIsBiggerThanP(ytrue, ypredict, requiredPrecision):
	""" To be implemented
	"""
	pass


def adjustedAverageNPV(ytrue, ypredict, requiredPrecision):
	""" To be implemented
	"""
	pass

