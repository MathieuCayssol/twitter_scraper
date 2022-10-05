from http import client
from pydoc import cli
import os
from tracemalloc import start
from typing import Dict
import tweepy

from scraper import Scraper
import config
import datetime
import pandas as pd
import time

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID'),
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')

time. sleep(60)

try:
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
except:
    print("Client error, check your bearer token or tweepy documentation")

def create_time_range()-> tuple[datetime.datetime, datetime.datetime]:
    current = datetime.datetime.now()
    round_min = 15*(current.minute // 15)
    end_date = datetime.datetime(
        year=current.year,
        month=current.month,
        day=current.day, 
        hour=current.hour,
        minute=round_min
    )
    start_date = end_date - datetime.timedelta(minutes=15)
    return start_date, end_date

start_date, end_date = create_time_range()
filename = "twitter_{}_to_{}.parquet".format(start_date, end_date)


A = Scraper(
    config=config,
    client=client
)

raw_data = A.get_tweets(start_date=start_date, end_date=end_date)
df = A.transform_data(raw_data)
df.to_parquet(filename)
A.export_data(
    key_id=AWS_ACCESS_KEY_ID,
    access_key=AWS_SECRET_ACCESS_KEY,
    file_name=filename
)



