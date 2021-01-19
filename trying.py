from polygon.PolygonRestApi import PolygonRestApi
from datetime import datetime 

p = PolygonRestApi()


dr = p.get_agregate_bars("AAPL", datetime(2020,10,14), datetime(2020,10,14), multiplier=1, timespan='minute')
print(dr.head())