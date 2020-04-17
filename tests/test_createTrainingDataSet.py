import sys
sys.path.append('/Users/lduque/Desktop/myProjects/moneyManager/')
import unittest
from datetime import datetime
from datetime import timedelta
import numpy as np
from stockModel.createTrainingDataSet import createFeaturesAtCurrentTime
from stockModel.createTrainingDataSet import createTrainingDataSet

class Test_createTrainingDataSet(unittest.TestCase):
    def test_returnsAllTheSamplesIfTimeSeriesIsConsecutive(self):
        numSamples, currentTime = 10, datetime(2019,1,3,15,0)
        pastLen, futureLen = 3, 3
        X, y = createTrainingDataSet('GS', numSamples, currentTime, pastLen, futureLen, dropDateColumns=False)
        expectedSamples = numSamples-pastLen-futureLen+1
        self.assertEqual(len(X), expectedSamples)
        self.assertEqual(len(y), expectedSamples)

    def test_returnsLessSamplesIfTimeSeriesIsNotConsecutive(self):
        numSamples, currentTime = 10, datetime(2019,1,3,14,33)
        pastLen, futureLen = 3, 3
        X,y = createTrainingDataSet('GS', numSamples, currentTime, pastLen, futureLen, dropDateColumns=False)
        expectedSamples = numSamples-pastLen-futureLen+1
        self.assertTrue(len(X)<expectedSamples)
        self.assertTrue(len(y)<expectedSamples)

    def test_lastDateReturnedMustBeBeforeEndTime(self):
        numSamples, currentTime = 10, datetime(2019,1,3,15,0)
        pastLen, futureLen = 3, 3
        X, y = createTrainingDataSet('GS', numSamples, currentTime, pastLen, futureLen, dropDateColumns=False)
        lastDateX = X.date.values[-1][-1]
        lastDatey = y.date.values[-1][-1]
        self.assertTrue(lastDateX<currentTime)
        self.assertTrue(lastDatey<currentTime)

    def test_indexCompatibleWithDateinY(self):
        numSamples, currentTime = 10, datetime(2019,1,3,15,0)
        pastLen, futureLen = 3, 3
        X, y = createTrainingDataSet('GS', numSamples, currentTime, pastLen, futureLen, dropDateColumns=False)
        indexY = y.index.values
        firstFutureDate = y.date.apply(lambda x: x[0]).values
        self.assertTrue([indexY[i]==firstFutureDate[i] for i in range(len(y))])


    def test_indexCompatibleWithDateinX(self):
        numSamples, currentTime = 10, datetime(2019,1,3,15,0)
        pastLen, futureLen = 2, 2
        X, y = createTrainingDataSet('GS', numSamples, currentTime, pastLen, futureLen, dropDateColumns=False)
        indexX = X.index.values
        lastFeatureDatePlusOneMinute = X.date.apply(lambda x: x[-1]).apply(lambda x:x+timedelta(minutes=1))
        self.assertTrue([indexX[i]==lastFeatureDatePlusOneMinute for i in range(len(X))])


class Test_createFeaturesAtCurrentTime(unittest.TestCase):
    def test_returnsNoneWhenNotEnoughConsecutiveSamples(self):
        currentTime = datetime(2019,1,3,14,33)
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastLen=4, dropDateColumns=False)
        self.assertIsNone(df)

    def test_returnsDfWhenConsecutiveSamplesAreAvailable(self):
        currentTime = datetime(2019,1,3,15,0)
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastLen=4, dropDateColumns=False)
        self.assertEqual(len(df), 1)

    def test_featureSizeMatchesPastStart(self):
        currentTime = datetime(2019,1,3,15,0)
        pastLen = 5
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastLen=pastLen, dropDateColumns=False)
        self.assertEqual(len(df.date.values[0]), pastLen)

    def test_indexMatchesCurrentTime(self):
        currentTime = datetime(2019,1,3,15,0)
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastLen=4, dropDateColumns=False)
        index = df.index.values[0]
        self.assertEqual(index, np.datetime64(currentTime))

    def test_indexIsConsistentWithFeatureDates(self):
        currentTime = datetime(2019,1,3,15,0)
        pastLen = 4
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastLen=pastLen, dropDateColumns=False)
        index = df.index.values[0]
        firstDate = df.date.values[0][0]
        self.assertEqual(index, np.datetime64(firstDate + timedelta(minutes=pastLen)))
        lastDate = df.date.values[0][-1]
        self.assertEqual(index, np.datetime64(lastDate+timedelta(minutes=1)))

if __name__ == '__main__':
    unittest.main()