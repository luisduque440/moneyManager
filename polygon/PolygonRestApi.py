import requests
from datetime import datetime
import pandas as pd

class PolygonRestApi():
    def __init__(self):
        self.apiKey = "b5h6i15Km42SVDlGJHeyUmwxcyR4LKfr"
        pass

    def get_agregate_bars(self, ticker, start_date, end_date,  multiplier=1, timespan='day'):
        endpointBase = "https://api.polygon.io/v2/aggs/"
        endpointEnd = "ticker/{ticker}/range/{multiplier}/{timespan}/{start}/{end}"
        endpointEnd = endpointEnd.replace("{ticker}", ticker)
        endpointEnd = endpointEnd.replace("{multiplier}", str(multiplier))
        endpointEnd = endpointEnd.replace("{timespan}", timespan)
        endpointEnd = endpointEnd.replace("{start}", start_date.strftime("%Y-%m-%d"))
        endpointEnd = endpointEnd.replace("{end}", start_date.strftime("%Y-%m-%d"))
        endpoint = endpointBase + endpointEnd
        print(endpoint)

        query = {
            'unadjusted':'true',
            'sort':'asc',
            'limit':'50000', 
            'apiKey': self.apiKey 
            }

        response = requests.get(endpoint, params=query) #params=query
        print(response)
        print(response.json())
        response = response.json()
        queryCount = response['queryCount']
        resultsCount = response['resultsCount']
        status = response['status']
        request_id= response['request_id']
        count= response['count']

        results = response['results']
        results_series = [pd.Series(r) for r in results]
        # should be better with append
        dr = pd.concat(results_series, axis=1).T


        print('qC=', queryCount)
        return dr





    
