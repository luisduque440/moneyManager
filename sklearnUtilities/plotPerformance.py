import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score
from .precisionRecallUtilities import getPrecisionRecallAlpha
from .precisionRecallUtilities import averageAlpha
from .precisionRecallUtilities import selectThreshold


def plotPerformance(ytrain, ytrainScores, ytest, ytestScores, requiredPrecision=0.55, requiredRecall=None, requiredCertainty=0.9):
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
	chosenPrecision, chosenRecall, chosenThreshold, chosenAlpha = selectThreshold(ytest, ytestScores, requiredPrecision, requiredRecall, requiredCertainty)

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



