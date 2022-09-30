from http import client
from pydoc import cli
import os
from typing import Dict
import tweepy

from scraper import Scraper
import config

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

try:
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
except:
    print("Client error, check your bearer token or tweepy documentation")

A = Scraper(
    config=config,
    client=client
)

A.extract_ids_name()
