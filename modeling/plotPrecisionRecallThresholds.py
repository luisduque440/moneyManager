from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
import matplotlib.pyplot as plt

import pandas as pd
import random
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
from scipy.stats import beta

# include base rate asap in ALL the plots !

def plotProbabilityOfPrecisionBiggerThan60p(scores, outcomes):
    df = pd.DataFrame({'outcomes':outcomes, 'scores': scores})
    df['counter']=1
    df.outcomes= df.outcomes.apply(int)
    df = df.sort_values(by='scores', ascending=False)
    so = df.groupby('scores')['outcomes'].sum()
    sc = df.groupby('scores')['counter'].sum()
    dg = pd.concat([so,sc],axis=1)
    dg = dg.sort_index(ascending=False)
    dc = dg.cumsum()
    dc.columns = ['k', 'N']
    dc['precision']=dc.k/dc.N
    dc['recall']=dc.k/dc.k.max()
    dc['P(precision)>0.6']=dc.apply(lambda x: 1-beta.cdf(0.6, 1+x.k, 1+x.N-x.k), axis=1)
    dc['P(precision)>0.6'].plot(title='Probability that the precision is bigger than 60% at each threshold')
    plt.xlabel('threshold')
    plt.show()


def plotPrecisionRecallThresholds(model, Xtrain, ytrain, Xtest, ytest):
    """ asdfks
    """
    disp = plot_precision_recall_curve(model, Xtrain, ytrain)
    disp.ax_.set_xlim(0.0, 0.5);
    disp.ax_.set_ylim(0.4, 1.0);
    disp.ax_.set_title('precision - recall in train data set');


    disp = plot_precision_recall_curve(model, Xtest, ytest);
    disp.ax_.set_xlim(0.0, 0.5);
    disp.ax_.set_ylim(0.4, 1.0);
    disp.ax_.set_title('precision - recall in test data set');
    plt.show()
    
    precisionTrain, recallTrain, thresholds = precision_recall_curve(ytrain, model.predict_proba(Xtrain)[:,1])
    thresholdsTrain = list(thresholds)+[1.0]
    precisionTest, recallTest, thresholds = precision_recall_curve(ytest, model.predict_proba(Xtest)[:,1])
    thresholdsTest = list(thresholds)+[1.0]

    plt.title('recall vs precision on train and test sets')
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.plot(recallTrain, precisionTrain, label='train')
    plt.plot(recallTest, precisionTest, label='test')
    legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.xlim(0.0,0.1)
    plt.show()

    plt.title('threshold vs recall on train and test sets')
    plt.xlabel('threshold')
    plt.ylabel('recall')
    plt.plot(thresholdsTrain, recallTrain, label='train')
    plt.plot(thresholdsTest, recallTest, label='test')
    legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.show()

    plt.title('threshold vs precision on train and test sets')
    plt.xlabel('threshold')
    plt.ylabel('precision')
    plt.plot(thresholdsTrain, precisionTrain, label='train')
    plt.plot(thresholdsTest, precisionTest, label='test')
    legend = plt.legend(loc='upper left', shadow=True, fontsize='x-large')
    plt.show()
    
    plotProbabilityOfPrecisionBiggerThan60p(model.predict_proba(Xtest)[:,1], ytest)
    
    
    
    
