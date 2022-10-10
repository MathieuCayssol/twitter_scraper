import os
from tracemalloc import start
from typing import Dict
import tweepy

from scraper import Scraper
import datetime
import pandas as pd
import time
import boto3

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID'),
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')

twitter_account = list(
    pd.read_csv("data/Top10000Journos.csv")
        .sort_values(by="total_followers", ascending=False)
        .reset_index(drop=True)["username"]
    )

#time.sleep(60)

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
filename = "twitter_{}_to_{}.csv".format(start_date, end_date)


A = Scraper(
    twitter_account=twitter_account,
    client=client
)

raw_data = A.get_tweets(start_date=start_date, end_date=end_date)
df = A.transform_data(raw_data)
df.to_csv(filename)


client_s3 = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
client_s3.upload_file(Filename=filename,
    Bucket='mathieu-data',
    Key=filename
)



