# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 09:48:49 2021

@author: Tirth Patel
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd

analyzer = SentimentIntensityAnalyzer()

tweet = pd.read_excel('A:/SA/DATA/test1.xlsx')

tweet = tweet.astype({"Text":str})
 
tweet['VADER Polarity'] = [analyzer.polarity_scores(i)['compound'] for i in tweet['Text']]
tweet['TextBlob Subjectivity'] = [TextBlob(i).sentiment.subjectivity for i in tweet['Text']]

tweet.to_excel('A:/SA/DATA/test1.xlsx', index=False)