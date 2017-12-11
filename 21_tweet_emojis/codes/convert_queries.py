import csv
import pickle
import re

'''
This file was used for preprocessing of the queried tweets.
We pulled them down directly (without first inserting into our database).
so we first redo the same preprocessing
'''
# the first 11 tweets
#dat = pickle.load(open('queried_tweets/tweets.p', 'rb')) 
# after that, we grabbed 5 more to make an even 4x4 oh histograms
dat = pickle.load(open('queried_tweets/tweets3.p', 'rb'))

HAPPY_EMOJI = {
    '☺️': 1,
    ':)': 2,
    '😍': 3,
}

SAD_EMOJI = {
    '☹️': -1,
    '😞': -1,
    ':(': -2,
    '😢': -3,
}

POSITIVE_STRING_SET = set(HAPPY_EMOJI.keys())
NEGATIVE_STRING_SET = set(SAD_EMOJI.keys())

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    cleaned = ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())

    if cleaned[0:3] == 'RT ':
        cleaned = cleaned[3:]
    return cleaned

for key in dat.keys():
    f = open('queried_tweets/first_pass_preprocess/{}_first_pass.csv'.format(key), 'w')
    #w = csv.writer(f)

    for tweet in dat[key]:

        # saving text of tweet
        

        f.write('"{0}","0"\n'.format(clean_tweet(tweet.text)))

f.close()
