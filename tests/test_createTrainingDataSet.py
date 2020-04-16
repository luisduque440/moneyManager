import sys
sys.path.append('/Users/lduque/Desktop/myProjects/moneyManager/')
import unittest
from datetime import datetime
from datetime import timedelta
from stockModel.createTrainingDataSet import createFeaturesAtCurrentTime
from stockModel.createTrainingDataSet import createTrainingDataSet
#from loadData.loadTimeSeries import getAvailableMarketMinutes
#print(getAvailableMarketMinutes()[:200])
class Test_createTrainingDataSet(unittest.TestCase):

    def test_returnsAllTheSamplesIfTimeSeriesIsConsecutive(self):
        numSamples, currentTime = 10, datetime(2019,1,1,11,0)
        pastStarts, futureEnds = 3, -3
        X, y = createTrainingDataSet('GS', numSamples, currentTime, pastStarts, futureEnds)
        expectedSamples = numSamples-pastStarts-futureEnds
        self.assertEqual(len(X), expectedSamples)
        self.assertEqual(len(y), expectedSamples)

    def test_returnsLessSamplesIfTimeSeriesIsNotConsecutive(self):
        numSamples, currentTime = 10, datetime(2019,1,1,10,0)
        pastStarts, futureEnds = 3, -3
        X,y = createTrainingDataSet('GS', numSamples, currentTime, pastStarts, futureEnds)
        self.assertTrue(len(X)<numSamples-pastStarts-futureEnds)
        self.assertTrue(len(y) < numSamples - pastStarts - futureEnds)

    def test_lastDateReturnedMustBeBeforeEndTime(self):
        numSamples, currentTime = 10, datetime(2019,1,2,14,40)
        pastStarts, futureEnds = 3, -3
        X, y = createTrainingDataSet('GS', numSamples, currentTime, pastStarts, futureEnds)
        lastDateX = X.date.values[-1][-1]
        lastDatey = y.date.values[-1][-1]
        self.assertTrue(lastDateX<currentTime)
        self.assertTrue(lastDatey<currentTime)

class Test_createFeaturesAtCurrentTime(unittest.TestCase):
    def test_returnsNoneWhenMarketOpens(self):
        currentTime = datetime(2019,1,2,14,31)
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastStarts=5)
        self.assertIsNone(df)

    def test_returnsDataFrameAWhileAfterOpening(self):
        currentTime = datetime(2019,1,2,14,40)
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastStarts=5)
        self.assertTrue(len(df)==1)

    def test_dateFieldMatchesIndex(self):
        currentTime = datetime(2019,1,2,14,40)
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastStarts=5)
        index = df.index.values[0]
        lastDate = df.date.values[0][-1]
        self.assertEqual(index, lastDate)

    def test_indexDateIsJustBeforeCurrentTime(self):
        currentTime = datetime(2019,1,2,14,40)
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastStarts=5)
        index = df.index.values[0]
        expectedIndex = currentTime - timedelta(minutes=1)
        self.assertEqual(index, expectedIndex)

if __name__ == '__main__':
    unittest.main()
