"""After updating Scraping List, Transcripts database
Run question1n2.py to feed latest companies to Claude API
"""

import pandas as pd
import json
import datetime, time
from question1n2 import main
EarningsTranscriptList = './db/EarningsTranscriptList.csv'
q1_DB = './db/question1.json'
Q1_DB_hist = json.load(open(q1_DB, 'r'))

# Start date for the feed
startDate = datetime.date(2023,5,31)

df = pd.read_csv(EarningsTranscriptList)
df['publish_date'] = pd.to_datetime(df['publish_date']).apply(lambda x: x.date())

tickers2feed = df[['Ticker','date']][df['publish_date']>=startDate]
tickers2feed['date'] = tickers2feed['date'].apply(lambda x: str(pd.Timestamp(x).date()).replace('-',''))

for i in tickers2feed.index:
    ticker = tickers2feed.loc[i,'Ticker']
    dateStr = tickers2feed.loc[i,'date']

    if ticker+dateStr not in Q1_DB_hist.keys():
        print(f'Feeding ticker: {ticker} for {dateStr}')
        qtrSelect = '2'
        modelSelect = "claude-v1.3-100k"
        main(ticker,dateStr,qtrSelect,modelSelect)
        print('Moving on to next stock')
        time.sleep(20)
