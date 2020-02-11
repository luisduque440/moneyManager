import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
from scipy.stats import beta
from sklearn.metrics import average_precision_score


# all the inputs are

def getPrecisionRecallAlpha(y, scores, P=0.6):
	""" re
	"""
	df = pd.DataFrame({'y':y, 'scores': scores})
	df['counter']=1
	df.y= df.y.apply(int)
	dg = df.groupby('scores')['y', 'counter'].sum().sort_index(ascending=False).cumsum()
	dg.columns = ['k', 'N']
	dg['precision']=dg.k/dg.N
	dg['recall']=dg.k/dg.k.max()
	dg['alphaProbability']=dg.apply(lambda x: 1-beta.cdf(P, 1+x.k, 1+x.N-x.k), axis=1)
	return dg.precision.values, dg.recall.values, dg.index.values, dg.alphaProbability.values


def getPrecisionRecall(y, scores):
	""" maybe not even using this
	"""
	precision, recall, threshold, _ = getPrecisionRecallAlpha(y, scores)
	return precision, recall, threshold


def averageAlpha(ytrue, yScores, P):
	""" To be implemented
	"""
	_, _, _, alpha = getPrecisionRecallAlpha(ytrue, yScores)
	return np.mean(alpha)



def getNpvTnrThreshold(ytrue, ypredicted):
	""" To be implemented
	"""
	pass




def getProbabilityNpvIsBiggerThanP(ytrue, ypredict, P):
	""" To be implemented
	"""
	pass


def adjustedAverageNPV(ytrue, ypredict, P):
	""" To be implemented
	"""
	pass

def plotTrainTestPrecisionRecall(ytrain, ytrainScores, ytest, ytestScores, P=0.6):
	""" Comment
	"""
	precisionTrain, recallTrain, thresholdTrain, alphaTrain = getPrecisionRecallAlpha(ytrain, ytrainScores)
	precisionTest, recallTest, thresholdTest, alphaTest = getPrecisionRecallAlpha(ytest, ytestScores)
	averageAlphaTrain = averageAlpha(ytrain, ytrainScores, P)
	averageAlphaTest = averageAlpha(ytest, ytestScores, P)
	baseRateTrain = sum(ytrain)/len(ytrain)
	baseRateTest = sum(ytest)/len(ytest)
	apTrain = average_precision_score(ytrain, ytrainScores)
	apTest = average_precision_score(ytest, ytestScores)

	plt.plot(recallTrain, precisionTrain, label='train (auc=%1.2f)' %(apTrain))
	plt.plot(recallTest, precisionTest, label='test (auc=%1.2f)'%(apTest))
	plt.plot([0,1], [baseRateTest, baseRateTest], 'b-', label='base rate (%1.2f)' %(baseRateTest))
	plt.title('precision recall curve')
	plt.xlabel('recall')
	plt.ylabel('precision')
	plt.legend(loc='lower right', shadow=True)
	plt.show()

	plt.title('Probability that the precision is bigger than 60 percent')
	plt.xlabel('threshold')
	plt.ylabel('probability')
	plt.plot(thresholdTrain, alphaTrain, label='train '+'(average alpha=%1.2f)'%(averageAlphaTrain))
	plt.plot(thresholdTest, alphaTest, label='test '+'(average alpha=%1.2f)'%(averageAlphaTest))
	plt.legend(loc='upper left', shadow=True)
	plt.show()


def plotTrainTestPrecisionRecallUsingModel(model, Xtrain, ytrain, Xtest, ytest, P=0.6):
	ytrainScores = model.predict_proba(Xtrain)[:,1]
	ytestScores = model.predict_proba(Xtest)[:,1]
	plotTrainTestPrecisionRecall(ytrain, ytrainScores, ytest, ytestScores, P)







