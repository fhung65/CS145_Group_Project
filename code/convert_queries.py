import csv
import pickle
import re

#dat = pickle.load(open('tweets.p', 'rb'))
dat = pickle.load(open('tweets3.p', 'rb'))

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
    f = open('{}_first_pass.csv'.format(key), 'w')
    #w = csv.writer(f)

    for tweet in dat[key]:

        # saving text of tweet
        

        f.write('"{0}","0"\n'.format(clean_tweet(tweet.text)))

f.close()
