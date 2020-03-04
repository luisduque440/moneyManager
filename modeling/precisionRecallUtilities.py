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


def selectThreshold(y, scores, requiredPrecision, requiredCertainty):
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

def plotTrainTestPrecisionRecall(ytrain, ytrainScores, ytest, ytestScores, requiredPrecision=0.55, requiredCertainty=0.9):
	""" Comment
	"""
	precisionTrain, recallTrain, thresholdTrain, alphaTrain = getPrecisionRecallAlpha(ytrain, ytrainScores, requiredPrecision)
	precisionTest, recallTest, thresholdTest, alphaTest = getPrecisionRecallAlpha(ytest, ytestScores, requiredPrecision)
	averageAlphaTrain = averageAlpha(ytrain, ytrainScores, requiredPrecision)
	averageAlphaTest = averageAlpha(ytest, ytestScores, requiredPrecision)
	baseRateTrain = sum(ytrain)/len(ytrain)
	baseRateTest = sum(ytest)/len(ytest)
	apTrain = average_precision_score(ytrain, ytrainScores)
	apTest = average_precision_score(ytest, ytestScores)
	chosenPrecision, chosenRecall, chosenThreshold, chosenAlpha = selectThreshold(ytest, ytestScores, requiredPrecision, requiredCertainty)

	plt.plot(recallTrain, precisionTrain, label='train (auc=%1.2f)' %(apTrain))
	plt.plot(recallTest, precisionTest, label='test (auc=%1.2f)'%(apTest))
	plt.plot([0,1], [baseRateTest, baseRateTest], 'b-', label='base rate (%1.2f)' %(baseRateTest))
	if chosenRecall!=None:
		label = 'operating point (precision=%3.2f)(recall=%3.2f)' %(chosenPrecision, chosenRecall)
		plt.plot([chosenRecall,chosenRecall], [0, 1], 'b--', label=label)
	plt.title('precision recall curve')
	plt.xlabel('recall')
	plt.ylabel('precision')
	plt.legend(loc='lower right', shadow=True)
	plt.show()


	plt.plot(thresholdTrain, alphaTrain, label='train '+'(average alpha=%1.2f)'%(averageAlphaTrain))
	plt.plot(thresholdTest, alphaTest, label='test '+'(average alpha=%1.2f)'%(averageAlphaTest))
	if chosenThreshold!=None:
		label = 'operating point (precision=%3.2f)(recall=%3.2f)' %(chosenPrecision, chosenRecall)
		plt.plot([chosenThreshold,chosenThreshold], [0, 1], 'b--', label=label)
	plt.title('Probability that the precision is bigger than %3.2f %%'%(100*requiredPrecision))
	plt.xlabel('threshold')
	plt.ylabel('probability')
	plt.legend(loc='upper left', shadow=True)
	plt.show()

def plotTrainTestPrecisionRecallUsingModel(model, Xtrain, ytrain, Xtest, ytest, requiredPrecision=0.55, requiredCertainty=0.9):
	ytrainScores = model.predict_proba(Xtrain)[:,1]
	ytestScores = model.predict_proba(Xtest)[:,1]
	plotTrainTestPrecisionRecall(ytrain, ytrainScores, ytest, ytestScores, requiredPrecision, requiredCertainty)







