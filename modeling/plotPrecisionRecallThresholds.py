from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
import matplotlib.pyplot as plt

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
