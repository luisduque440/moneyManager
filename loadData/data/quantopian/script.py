
import pandas as pd 

for i in range(1,7):
	print(i)
	df=pd.read_csv('SixPieces/piece%d.csv'%(i))
	symbols = list(df.symbol.unique())
	for s in symbols: df[df.symbol==s].to_csv('minuteIntraday/'+s+'.csv', index=False)
