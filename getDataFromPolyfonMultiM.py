from polygon import RESTClient
import pandas as pd
from datetime import datetime, timedelta

stockName = 'COIN'
timeFrame = 15
unit = 'second'
fromDate = '2019-01-01'
toDate = '2019-12-01'

def polygon_request(ticker, multiplier, timespan, start, end):
    client = RESTClient(api_key="7PZTsP8NHCZy0cEsWRlgFaSa2Q8zm8Zb")
    aggs = []
    for a in client.list_aggs(ticker=ticker, multiplier=multiplier, timespan=timespan, from_=start, to=end, limit=50000):
        aggs.append(a)
    df = pd.DataFrame(aggs)
    df.index = pd.DatetimeIndex(pd.to_datetime(df.timestamp, unit='ms', utc=True)).tz_convert('US/Eastern')
    df.drop(['timestamp', 'transactions', 'otc'], axis=1, inplace=True)
    return df

def split_by_month(df, ticker, multiplier, unit):
    df =df.sort_index()
    
    for (year, month), group in df.groupby([df.index.year, df.index.month]):
        dfName = f"{ticker}-{multiplier}{unit}-{year}-{str(month).zfill(2)}.csv"
        
        group.to_csv(dfName)
        print(f"Saved {dfName} Done")

# df = polygon_request(stockName, timeFrame, unit, fromDate, toDate)

# df.to_csv(f"{stockName}-{timeFrame}{unit}-{fromDate}-to-{toDate}.csv")

startDate = datetime.strptime(fromDate, "%Y-%m-%d")
endDate = datetime.strptime(toDate, "%Y-%m-%d")

currentStart = startDate
while currentStart <= endDate:
    currentEnd = (currentStart+timedelta(days=31)).replace(day=1)-timedelta(seconds = 1)
    currentEnd = min(currentEnd, endDate)
    
    df = polygon_request(stockName, timeFrame, unit, currentStart.strftime("%Y-%m-%d"), currentEnd.strftime("%Y-%m-%d"))
    split_by_month(df, stockName, timeFrame,unit)
    
    currentStart = (currentStart+timedelta(days=31)).replace(day=1)
