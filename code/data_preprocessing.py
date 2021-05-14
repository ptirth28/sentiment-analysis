import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
import numpy as np
import pandas as pd
import spacy
import re
import emoji
from nltk.corpus import stopwords
import en_core_web_lg
from textblob import TextBlob
from collections import Counter

total_data = pd.read_csv("8k_annotations.csv", encoding="ISO-8859-1")
total_data['Text'] = total_data['Text'].apply(str)
total_data['Original Text'] = total_data['Text']
total_data = total_data.dropna()

contractions = { 
"ain't": "am not / are not / is not / has not / have not",
"aren't": "are not / am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"I'd": "I had / I would",
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I shall have / I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}

ner = en_core_web_lg.load()
STOPWORDS = set(stopwords.words('english'))
cnt = Counter()
final_text_lst = []

def process_tweet(tweet):
    tweet = emoji.demojize(tweet)                                     # Converting emojis to words
    tweet = tweet.lower()                                             # Lowercases the string
    tweet = re.sub('@[^\s]+', '', tweet)                              # Removes usernames
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', tweet)   # Remove URLs
    tweet = re.sub(r"\d+", " ", str(tweet))                           # Removes all digits
    tweet = re.sub('&quot;'," ", tweet)                               # Remove (&quot;)                                            
    tweet = re.sub(r"\b[a-zA-Z]\b", "", str(tweet))                   # Removes all single characters
    for word in tweet.split():
        if word.lower() in contractions:
            tweet = tweet.replace(word, contractions[word.lower()])   # Replaces contractions
    tweet = re.sub(r"[^\w\s]", " ", str(tweet))                       # Removes all punctuations
    tweet = re.sub(r'(.)\1+', r'\1\1', tweet)                         # Convert more than 2 letter repetitions to 2 letter
    tweet = re.sub(r"\s+", " ", str(tweet))                           # Replaces double spaces with single space    
    return tweet

# Function to remove stopwords
def stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

# Function to remove frequent words
def freqwords(text):
    return " ".join([word for word in str(text).split() if word not in freq])

# Function to remove rare words
def rarewords(text):
    return " ".join([word for word in str(text).split() if word not in rare])

# Preprocessing tweets
total_data['Text'] = np.vectorize(process_tweet)(total_data['Text'])

# Removing stopwords
total_data['Text'] = total_data['Text'].apply(stopwords)

# Removing frequent words
for text in total_data['Text'].values:
    for word in text.split():
        cnt[word] += 1
freq = set([w for (w, wc) in cnt.most_common(10)])
total_data['Text'] = total_data['Text'].apply(freqwords)

# Removing rare words
rare = pd.Series(' '.join(total_data['Text']).split()).value_counts()[-10:] # 10 rare words
rare = list(rare.index)
total_data['Text'] = total_data['Text'].apply(rarewords)

# Removing names
for index, row in total_data.iterrows():
    text_data = row['Text']
    t = ner(text_data)
    final_text_lst.append(" ".join([ent.text for ent in t if not ent.ent_type_]))
total_data['Text'] = final_text_lst

# Spell check
total_data['Text'].apply(lambda x: str(TextBlob(x).correct()))

total_data.rename(columns={'Text' : 'Preprocessed Text'})

total_data.to_csv("8k annotation preprocessed.csv", index=False)
