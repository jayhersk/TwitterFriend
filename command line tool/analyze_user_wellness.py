# analyze the wellness score for one user

import json
import os

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def split_data(data):
    split_data = {}

    for tweet in data['tweets']:
        month_string = tweet['created'][3:11]
        if month_string not in split_data.keys():
            split_data[month_string] = {}
            split_data[month_string]['tweets'] = []
            split_data[month_string]['retweets'] = []
            split_data[month_string]['replies'] = []

        split_data[month_string]['tweets'].append(tweet)

    for tweet in data['retweets']:
        month_string = tweet['created'][3:11]
        if month_string not in split_data.keys():
            split_data[month_string] = {}
            split_data[month_string]['tweets'] = []
            split_data[month_string]['retweets'] = []
            split_data[month_string]['replies'] = []

        split_data[month_string]['retweets'].append(tweet)

    for tweet in data['replies']:
        month_string = tweet['created'][3:11]
        if month_string not in split_data.keys():
            split_data[month_string] = {}
            split_data[month_string]['tweets'] = []
            split_data[month_string]['retweets'] = []
            split_data[month_string]['replies'] = []

        split_data[month_string]['replies'].append(tweet)

    return split_data

# Return proportion of negative sentiment tweets
def sentiment_score(tweet_list):
    if len(tweet_list) > 0:
        analyzer = SentimentIntensityAnalyzer()
        neg_count = 0
        for tweet in tweet_list:
            vs = analyzer.polarity_scores(tweet['text'])
            # print("{:-<65} {}".format(tweet['text'], str(vs)))
            if vs['compound'] <= -0.05:
                neg_count += 1

        return neg_count / len(tweet_list)
    return 0.0

# Return proportion of tweets made in the middle of the night
def insomnia_index(tweet_list):
    pass

# Data is a dictionary with entries: tweets, retweets, and replies.
def calculate_wellness(data):

    # Get tweet score
    tweet_sentiment = sentiment_score(data['tweets'])
    tweet_score = tweet_sentiment

    # Get retweet score
    retweet_sentiment = sentiment_score(data['retweets'])
    retweet_score = retweet_sentiment

    # Get reply score
    reply_sentiment = sentiment_score(data['replies'])
    reply_score = reply_sentiment

    return 0.5*tweet_score + 0.25*retweet_score + 0.25*reply_score

def user_wellness(username, friendname):
    # should return a dictionary that gives a wellness score for each week
    # and each month that the user was active.

    # Read tweet data
    data_path = os.path.join(os.path.join(username, 'friend_data'), friendname + '.json')
    data = {}
    with open(data_path) as data_json:
        data = json.load(data_json)

    # Split tweets into time intervals (weeks and months)
    data = split_data(data)

    # Create output dictionary
    wellness_scores = dict.fromkeys(data.keys())

    # Pass data intervals to function for calculating wellness
    for month in data.keys():
        wellness_scores[month] = calculate_wellness(data[month])

    return wellness_scores

if __name__ == '__main__':
    # pass in the username of the account you want to download
    data = user_wellness("jayhersk", "jayhersk")

    # write the json file
    with open("jayhersk" + '_wellness.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)

