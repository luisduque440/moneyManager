import unittest
import sys
from datetime import datetime
from datetime import timedelta
sys.path.append('/Users/lduque/Desktop/myProjects/moneyManager/')

from stockModel.createTrainingDataSet import createFeaturesAtCurrentTime
from stockModel.createTrainingDataSet import createTrainingDataSet
from loadData.loadTimeSeries import getAvailableMarketMinutes


class Test_createTrainingDataSet(unittest.TestCase):

    def test_returnsAllTheSamplesIfTimeSeriesIsConsecutive(self):
        numSamples, currentTime = 100, datetime(2019,1,1,11,0)
        pastStarts, futureEnds = 5, 5
        df = createTrainingDataSet('GS', numSamples, currentTime, pastStarts, futureEnds)
        expectedSamples = numSamples-pastStarts-futureEnds
        self.assertEqual(len(df), expectedSamples)

    def test_returnsLessSamplesIfTimeSeriesIsNotConsecutive(self):
        numSamples, currentTime = 100, datetime(2019,1,1,10,0)
        pastStarts, futureEnds = 5, 5
        df = createTrainingDataSet('GS', numSamples, currentTime, pastStarts, futureEnds)
        self.assertTrue(len(df)<numSamples-pastStarts-futureEnds)

    def test_lastDateReturnedMustBeBeforeEndTime(self):
        numSamples, currentTime = 100, datetime(2019,1,1,11,0)
        pastStarts, futureEnds = 5, 5
        df = createTrainingDataSet('GS', numSamples, currentTime, pastStarts, futureEnds)
        lastDate = df.date.values[-1]
        self.assertTrue(lastDate<currentTime)


class Test_createFeaturesAtCurrentTime(unittest.TestCase):

        #2019-01-02 14:33:00

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
        print(getAvailableMarketMinutes()[:100])
        currentTime = datetime(2019,1,2,14,40)
        df = createFeaturesAtCurrentTime(stock='GS', currentTime=currentTime, pastStarts=5)
        index = df.index.values[0]
        expectedIndex = currentTime - timedelta(minutes=1)
        self.assertEqual(index, expectedIndex)

if __name__ == '__main__':
    unittest.main()
