import pandas as pd

# Dirty, should be changed in the future. The list of twitter account will be hard coded and modified by the user
twitter_account = list(pd.read_csv("data/Top10000Journos.csv").sort_values(by="total_followers", ascending=False).reset_index(drop=True)["username"].loc[:2000])