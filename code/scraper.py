import re
import tweepy
from tweepy import OAuthHandler
import json

import sys
sys.path.insert(0,'.')
import keys


# Taken from http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    
    POSITIVE_STRING_SET = set(['☺️', ':)'])
    NEGATIVE_STRING_SET = set(['☹️', ':('])

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
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
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

 
    def get_tweets(self, queries = None, count = 1000):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        if queries is None:
            queries = self.POSITIVE_STRING_SET | self.NEGATIVE_STRING_SET

        try:
            # call twitter api to fetch tweets
            fetched_tweets = []
            for q in queries:
                fetched_tweets += self.api.search(q = q, count = count, lang='en')
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = self.clean_tweet(tweet.text)
                if parsed_tweet['text'] == '':
                    continue
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet)
                if parsed_tweet['sentiment'] == 0.5:
                    continue
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(count = 10000)
    print(tweets)

    filename = 'sample_tweets.json'
    f = open(filename, 'w')
    for t in tweets:
        f.write(json.dumps(t)+'\n')
    f.close()
 
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 1]
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 0]
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
 
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
 
if __name__ == "__main__":
    # calling main function
    #main()
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(count = 10000)
    print(tweets)

    filename = 'sample_tweets.json'
    f = open(filename, 'w')
    for t in tweets:
        f.write(json.dumps(t)+'\n')
    f.close()
 
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 1]
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 0]
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
 
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
