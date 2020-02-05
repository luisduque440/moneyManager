import unittest

class Test_modelBlender(unittest.TestCase):
	def test_one(self):
		self.assertTrue(True)

	def test_two(self):
		self.assertTrue(False)
		
if __name__ == '__main__':
    unittest.main()




# Use the following in test_marketSimulator.py
#from .loadTimeSeries import loadTimeSeries
#def testCaseForModelSimulator():
	#S=loadTimeSeries('GS', datetime(2019,1,1), datetime(2020,1,1)).consolidated
	#positionTS=pd.Series(['GS']*len(S),index=S.index)
	#win = modelSimulator(positionTS, initialAmount=S.values[0])
	# S and win must be *almost* the same