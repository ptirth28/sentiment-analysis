# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 19:11:59 2021

@author: Tirth Patel
"""
import tweepy
import pandas as pd
import preprocessor as p

p.set_options(p.OPT.URL)

def preprocessing(tweet):
    tweet = p.clean(tweet)
    return tweet

api_key = "YUjbV05MDVZvQflMALiRXDcDc"
api_secret = "uePHRGrDF3ptyOpnXj78J6A5AKgByN1RGZG2Y1Xb4H6ivWFMeb"
access_token = "1029941797307408384-1kVBVyeAO6OA6y4dTgQNPlhBpQBSPu"
access_token_secret = "nPNgmEne6K59nUvhMrAcrHmVWY9HKYDnkGJXm0Q6mVdTW"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

tweets = []

keywords_df = pd.read_excel('A:/SA/first 100 players.xlsx')
Merged_df = pd.DataFrame()
# count = 100

for (i,j) in zip(keywords_df['Twitter'],keywords_df['Player']):  
    player_name = j   
    Twitter_id = i    
    try:
        tweets = api.user_timeline(screen_name = Twitter_id, lang = 'en', tweet_mode = 'extended', count = 100)
        tweets_list = [[j, tweet.created_at, tweet.id, tweet.source, tweet.truncated, tweet.in_reply_to_screen_name, tweet.full_text, tweet.user.name, tweet.user.screen_name, tweet.user.followers_count, tweet.user.friends_count, tweet.user.geo_enabled, tweet.user.verified, tweet.coordinates, tweet.retweet_count, tweet.favorite_count, tweet.lang] for tweet in tweets]
        tweets_df = pd.DataFrame(tweets_list,columns=['Player','Datetime', 'Tweet Id', 'Source', 'Truncated', 'In Reply to Screen Name', 'Text', 'User Name', 'Screen Name', 'Followers Count', 'Friends Count', 'Geo Enabled', 'Verified', 'Coordinates', 'Retweet Count', 'Favorite Count','Language'])
        Merged_df = pd.concat([Merged_df, tweets_df])
    except:
        print(player_name)

Merged_df['Text'] = Merged_df['Text'].apply(lambda x: preprocessing(x))
Merged_df.to_excel('A:/SA/DATA/test1.xlsx', index=False)
print('Done')
