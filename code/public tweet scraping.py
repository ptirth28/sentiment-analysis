# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 18:07:05 2021

@author: Tirth Patel
"""
import tweepy
import pandas as pd
import preprocessor as p

p.set_options(p.OPT.URL)

def preprocessing(tweet):
    tweet = p.clean(tweet)
    return tweet

api_key = ""
api_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

tweets = []

keywords_df = pd.read_excel('A:/SA/Player Twitter Accounts.xlsx')
Merged_df = pd.DataFrame()
count = 1000

for (i,j) in zip(keywords_df['Keywords'],keywords_df['Player']):  
    player_name = j       
    text_query = i +' -filter:retweets'
    try:
        tweets = tweepy.Cursor(api.search,q=text_query,lang = 'en', tweet_mode = 'extended').items(count)
        tweets_list = [[j, tweet.created_at, tweet.id, tweet.source, tweet.truncated, tweet.in_reply_to_screen_name, tweet.full_text, tweet.user.name, tweet.user.screen_name, tweet.user.followers_count, tweet.user.friends_count, tweet.user.geo_enabled, tweet.user.verified, tweet.coordinates, tweet.retweet_count, tweet.favorite_count, tweet.lang] for tweet in tweets]
        tweets_df = pd.DataFrame(tweets_list,columns=['Player','Datetime', 'Tweet Id', 'Source', 'Truncated', 'In Reply to Screen Name', 'Text', 'User Name', 'Screen Name', 'Followers Count', 'Friends Count', 'Geo Enabled', 'Verified', 'Coordinates', 'Retweet Count', 'Favorite Count','Language'])
        Merged_df = pd.concat([Merged_df, tweets_df])
    except:
        print(player_name)

Merged_df['Text'] = Merged_df['Text'].apply(lambda x: preprocessing(x))
Merged_df.to_excel('A:/SA/DATA/test.xlsx', index=False)
print('Done')



