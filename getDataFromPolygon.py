from polygon import RESTClient
import pandas as pd
from datetime import datetime, time
import numpy as np
import plotly.graph_objects as go

def polygon_request(ticker, multiplier, timespan, start, end):
    client = RESTClient(api_key="7PZTsP8NHCZy0cEsWRlgFaSa2Q8zm8Zb")
    aggs = []
    for a in client.list_aggs(ticker=ticker, multiplier=multiplier, timespan=timespan, from_=start, to=end, limit=50000):
        aggs.append(a)
    df = pd.DataFrame(aggs)
    df.index = pd.DatetimeIndex(pd.to_datetime(df.timestamp, unit='ms', utc=True)).tz_convert('US/Eastern')
    df.drop(['timestamp', 'transactions', 'otc'], axis=1, inplace=True)
    return df

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

stockName = 'TQQQ'
timeFrame = 15
unit = 'second'
fromDate = '2024-08-24'
toDate = '2024-08-24'

df = polygon_request(stockName, timeFrame, unit, fromDate, toDate)


df.to_csv(f"{stockName}-{timeFrame}{unit}-{fromDate}-to-{toDate}.csv")
