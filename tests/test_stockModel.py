import sys
sys.path.append('/Users/lduque/Desktop/myProjects/moneyManager/')
import unittest
from datetime import datetime
from stockModel import stockModel

class test_stockModel(unittest.TestCase):
    def fitWorks(self):
        model = stockModel('GS', 2, 2, 50)
        model.fit(datetime(2019,3,1))

    def predict_probaReturnsNoneWhenNotENoughData(self):
        model = stockModel('GS', 2, 2, 50)
        model.fit(datetime(2019,3,1))
        p = model.predict_proba(datetime(2019,1,3,14,0,0))
        self.assertIsNone(p)

    def predict_probaReturnsProbability(self):
        model = stockModel('GS', 2, 2, 50)
        model.fit(datetime(2019,3,1))
        p = model.predict_proba(datetime(2019,1,3,14,30,0))
        self.assertIsNone(p)

if __name__ == '__main__':
    unittest.main()
