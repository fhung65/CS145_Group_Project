import re
import tweepy
from tweepy import OAuthHandler
from langdetect import detect

import sys
sys.path.insert(0,'.')
import keys
import pdb
import MySQLdb


# Taken from http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/


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

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

EMOJI_TO_KEY = merge_two_dicts(HAPPY_EMOJI, SAD_EMOJI)

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    
    POSITIVE_STRING_SET = set(HAPPY_EMOJI.keys())
    NEGATIVE_STRING_SET = set(SAD_EMOJI.keys())

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = keys.CONSUMER_KEY 
        consumer_secret = keys.CONSUMER_SECRET 
        access_token = keys.ACCESS_TOKEN 
        access_token_secret = keys.ACCESS_TOKEN_SECRET 
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print('Error: Authentication Failed')
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        cleaned = ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())

        if cleaned[0:3] == 'RT ':
            cleaned = cleaned[3:]
        return cleaned
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        '''

        sentiment = 0.5

        for substring in self.POSITIVE_STRING_SET:
            if substring in tweet.text:
                sentiment += 0.5
                break
        for substring in self.NEGATIVE_STRING_SET:
            if substring in tweet.text:
                sentiment -= 0.5
                break
        return sentiment

    def extended_search(self, count=1000, page=1, *args, **kwargs):
        if 'lang' not in kwargs:
            kwargs['lang'] = 'en'
        tweets = self.api.search(count=count, *args, **kwargs)
        print(len(tweets))
        # if page < 3:
        #     new_tweets = self.extended_search(page = page + 1, *args, **kwargs)
        #     if new_tweets:
        #         tweets = new_tweets + tweets
        return tweets
 
    def get_tweets(self, queries = None, count = 1000):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        if queries is None:
            queries = self.POSITIVE_STRING_SET | self.NEGATIVE_STRING_SET

        try:
            # call twitter api to fetch tweets
            fetched_tweets = []
            for q in queries:
                tweets = self.extended_search(q = q, lang='en', count = count)
 
                # parsing tweets one by one
                for tweet in tweets:
                    # empty dictionary to store required params of a tweet
                    parsed_tweet = {}
     
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet)
                    if parsed_tweet['sentiment'] == 0.5:
                        continue

                    # saving text of tweet
                    parsed_tweet['text'] = self.clean_tweet(tweet.text)
                    if parsed_tweet['text'] == '':
                        continue

                    parsed_tweet['emoji'] = q
     
                    fetched_tweets.append(parsed_tweet)
 
            # return parsed tweets
            return fetched_tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print('Error : ' + str(e))

    def insert_tweets_into_db(self, tweets):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='emoji_tweets', use_unicode=True)
        conn.set_character_set('utf8')
        cursor = conn.cursor()

        for tweet in tweets:
            try:
                cursor.execute('INSERT INTO tweets VALUES (%s, %s)', (tweet['text'], EMOJI_TO_KEY[tweet['emoji']]))
                conn.commit()
            except Exception as e:
                print('Ignoring %s' % e)
        cursor.close()
        conn.close()
 
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(count = 100)
    api.insert_tweets_into_db(tweets)

    ptweets = []
    ntweets = []
    for tweet in tweets:
        if tweet['sentiment'] > 0.5:
            ptweets.append(tweet)
        else:
            ntweets.append(tweet)
    print('there are %d tweets' % len(tweets))
 
    # picking positive tweets from tweets
    # printing first 5 positive tweets
    print('\n\nPositive tweets: %d' % len(ptweets))
    for tweet in ptweets:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print('\n\nNegative tweets: %d' % len(ntweets))
    for tweet in ntweets:
        print(tweet['text'])
 
if __name__ == '__main__':
    main()
