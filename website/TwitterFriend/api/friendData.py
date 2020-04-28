import flask
import datetime
import json
import time
import tweepy

import re
import string
import statistics

import requests
from flask import request

import TwitterFriend

from TwitterFriend.api.util import forbidden_403
from TwitterFriend.api.util import CONTRACTIONS
from TwitterFriend.api.util import UNIGRAMS
from TwitterFriend.api.util import BIGRAMS
from TwitterFriend.api.util import TRIGRAMS

from TwitterFriend.model import model_get_friend_data
from TwitterFriend.model import model_does_friend_need_update
from TwitterFriend.model import model_has_friend_scores
from TwitterFriend.model import model_set_friend_stress

from TwitterFriend.model import model_save_wellness_scores
from TwitterFriend.model import model_get_wellness_scores

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

@TwitterFriend.app.route('/api/f/<int:fid_slug>/', methods=["GET"])
def friend_data(fid_slug):

    # Fancy message for invalid access
    if "username" not in flask.session:
        return forbidden_403()

    # User
    context = {}
    logname = flask.session["username"]
    context["logname"] = logname
    context["url"] = flask.request.path

    # If friend data has not been completed within the last 7 days:
    if model_does_friend_need_update(logname, fid_slug):

        # Fetch and process the data
        run_twitter_analysis(logname, fid_slug)

    # Return the data from DB
    friend = model_get_friend_data(logname, fid_slug)

    # Put in context and return
    context['fid'] = fid_slug
    context['f_username'] = friend['f_username']
    context['f_fullname'] = friend['f_fullname']
    context['stressed'] = friend['stressed']
    context['checked'] = friend['checked'] # TODO: FORMAT DATETIME?

    print(context)
    return flask.jsonify(**context)

def run_twitter_analysis(username, fid):

    # Get friend username from DB
    friend = model_get_friend_data(username, fid)
    f_username = friend['f_username']
    time_last_checked = friend['checked']

    # If we don't have data for the friend:
    data = {}
    if not model_has_friend_scores(fid):
        data = get_all_tweets(f_username)

    # If we do have some data for the friend:
    else:
        # Get the data since the 'created' date # TODO
        data = get_all_tweets(f_username)

    # Split tweets into time intervals (weeks and months)
    data = split_data(data)

    # Process Data:
    # Create output dictionary
    wellness_scores = dict.fromkeys(data.keys())

    # Pass data intervals to function for calculating wellness
    for month in data.keys():
        wellness_scores[month] = calculate_wellness(data[month])

    # Save Scores in database: (updating if needed)
    model_save_wellness_scores(fid, wellness_scores)

    # Proccess scores to determine if the user is stressed
    is_stressed = determine_stress(wellness_scores)

    # Update stress boolean, checked time
    model_set_friend_stress(fid, is_stressed, datetime.datetime.now())

    return

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    consumer_key = TwitterFriend.app.config['API_KEY']
    consumer_secret = TwitterFriend.app.config['API_SECRET']
    user_token = flask.session['token']

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(user_token[0], user_token[1])
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []	
    tweets = tweepy.Cursor(api.user_timeline, screen_name=screen_name, count=200).items()
    while True:
        try:
            tweet = next(tweets)
        except tweepy.TweepError:
            print("Reached API limit. Sleeping now.")
            time.sleep(60*15)
            tweet = next(tweets)
        except StopIteration:
            break

        # Append username/ fullname pair to list:
        alltweets.append(tweet)

    # PROCESSED JSON OUTPUT:

    # transform tweepy tweets into json
    # alltweets is list of type tweepy.models.Status
    tweets = [] #TODO Still includes some replies (for deleted tweets or private users)
    retweets = []
    replies = []

    # TODO full text of the tweet is not there
    for tweet in alltweets:

        tweet_info = {}
        tweet_info['id_str'] = tweet.id_str
        tweet_info['created'] = tweet.created_at.strftime("%d-%b-%Y (%H:%M:%S.%f)")

        if len(tweet.text) > 0:

            # clean tweet content:
            text = clean_tweet(tweet.text)
            tweet_info['text'] = text

            if tweet.retweeted == True:
                retweets.append(tweet_info)

            elif tweet.in_reply_to_screen_name != None:
                replies.append(tweet_info)

            # Catch replies to a deleted tweet or changed username
            # Need to check original text because @ mentions are cleaned from tweets
            elif len(tweet.text) > 0 and tweet.text[0] == '@':
                replies.append(tweet_info)

            else:
                tweets.append(tweet_info)

    data = {}
    data['tweets'] = tweets
    data['retweets'] = retweets
    data['replies'] = replies

    return data

def clean_tweet(text):
    # remove emoji characters/ other unicode characters
    text = ''.join(c for c in text if c in string.printable)

    word_list = text.split()
    new_word_list = []
    for word in word_list:
        # lowercase all
        new_word = word.lower()

        # separate contractions
        if new_word in CONTRACTIONS.keys():
            new_word_list.append(CONTRACTIONS[new_word][0])
            new_word_list.append(CONTRACTIONS[new_word][1])

        else:
            # remove links
            if len(new_word) > 4 and new_word[:4] == 'http':
                new_word = ''

            # remove @ mentions
            elif len(new_word) > 0 and new_word[0] == '@':
                new_word = ''

            # remove hashtags
            elif len(new_word) > 0 and new_word[0] == '#':
                new_word = ''

            # remove character sequence from retweets
            elif new_word == "rt":
                new_word = ''

            # remove all punctuation, leave only alphanumeric characters
            else:
                new_word = new_word.translate(str.maketrans('', '', string.punctuation))
                new_word_list.append(new_word)

    # combine list again separated by single spaces
    new_text = ' '.join(new_word_list)

    return new_text

def date_key(month_string):
    year = month_string[4:]
    month = ""
    if month_string[:3] == "Jan":
        month = "1"
    elif month_string[:3] == "Feb":
        month = "2"
    elif month_string[:3] == "Mar":
        month = "3"
    elif month_string[:3] == "Apr":
        month = "4"
    elif month_string[:3] == "May":
        month = "5"
    elif month_string[:3] == "Jun":
        month = "6"
    elif month_string[:3] == "Jul":
        month = "7"
    elif month_string[:3] == "Aug":
        month = "8"
    elif month_string[:3] == "Sep":
        month = "9"
    elif month_string[:3] == "Oct":
        month = "10"
    elif month_string[:3] == "Nov":
        month = "11"
    elif month_string[:3] == "Dec":
        month = "12"
    return year + " " + month

def split_data(data):
    split_data = {}

    for tweet in data['tweets']:
        month_string = date_key(tweet['created'][3:11])
        if month_string not in split_data.keys():
            split_data[month_string] = {}
            split_data[month_string]['tweets'] = []
            split_data[month_string]['retweets'] = []
            split_data[month_string]['replies'] = []

        split_data[month_string]['tweets'].append(tweet)

    for tweet in data['retweets']:
        month_string = date_key(tweet['created'][3:11])
        if month_string not in split_data.keys():
            split_data[month_string] = {}
            split_data[month_string]['tweets'] = []
            split_data[month_string]['retweets'] = []
            split_data[month_string]['replies'] = []

        split_data[month_string]['retweets'].append(tweet)

    for tweet in data['replies']:
        month_string = date_key(tweet['created'][3:11])
        if month_string not in split_data.keys():
            split_data[month_string] = {}
            split_data[month_string]['tweets'] = []
            split_data[month_string]['retweets'] = []
            split_data[month_string]['replies'] = []

        split_data[month_string]['replies'].append(tweet)

    return split_data

# Data is a dictionary with entries: tweets, retweets, and replies.
# Will be between 0 and 1. Closer to 1 means more stress
def calculate_wellness(data):

    # Get tweet score
    tweet_sentiment = sentiment_score(data['tweets'])
    tweet_insomia = insomnia_index(data['tweets'])
    tweet_lexicon = depression_lexicon_score(data['tweets'])
    tweet_score = tweet_sentiment*0.4 + tweet_insomia*0.2 + tweet_lexicon*0.4

    # Get retweet score
    retweet_sentiment = sentiment_score(data['retweets'])
    retweet_insomia = insomnia_index(data['retweets'])
    retweet_lexicon = depression_lexicon_score(data["retweets"])
    retweet_score = retweet_sentiment*0.4 + retweet_insomia*0.2 + retweet_lexicon*0.4

    # Get reply score
    reply_sentiment = sentiment_score(data['replies'])
    reply_insomia = insomnia_index(data['replies'])
    reply_lexicon = depression_lexicon_score(data['replies'])
    reply_score = reply_sentiment*0.4 + reply_insomia*0.2 + reply_lexicon*0.4

    return 0.5*tweet_score + 0.25*retweet_score + 0.25*reply_score

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
    if len(tweet_list) > 0:
        insomia_count = 0
        for tweet in tweet_list:
            if int(tweet['created'][14]) > 0 and int(tweet['created'][14]) < 6:
                insomia_count += 1
        return insomia_count / len(tweet_list)
    return 0.0

# Score of proportion of tweets containing a term from lexicon
def depression_lexicon_score(tweet_list):
    if len(tweet_list) > 0:
        num_unigram = 0
        num_bigram = 0
        num_ngram = 0

        uni = False
        bi = False
        tri = False

        for tweet in tweet_list:
            for string in UNIGRAMS:
                if string in tweet['text']:
                    uni = True
            for string in BIGRAMS:
                if string in tweet['text']:
                    bi = True
            for string in TRIGRAMS:
                if string in tweet['text']:
                    tri = True

            if uni:
                num_unigram +=1
            if bi:
                num_bigram += 1
            if tri:
                num_ngram += 1
        num_tweets = len(tweet_list)
        # Weight unigrams slightly less because they are more common
        return (num_unigram/num_tweets)*0.25 + (num_bigram/num_tweets)*0.35 + (num_ngram/num_tweets)*0.4

    return 0.0

def determine_stress(wellness_scores):

    temp_keys = wellness_scores.keys()
    recent_keys = most_recent_months(temp_keys) # 4 most recent keys

    # If the score for the most recent month is higher than 0.75 standard
    # deviation above the average score
    scores = list(wellness_scores.values())
    if (len(scores) > 1):
        average = statistics.mean(scores)
        std_dev = statistics.stdev(scores)

        if wellness_scores[recent_keys[0]] >= (average + 0.15*std_dev):
            return True

    # If the scores have been increasing for the past 4 months
    if (len(recent_keys) > 3):
        if (wellness_scores[recent_keys[0]] >= wellness_scores[recent_keys[1]]) and (wellness_scores[recent_keys[1]] >= wellness_scores[recent_keys[2]]) and ((wellness_scores[recent_keys[2]] >= wellness_scores[recent_keys[3]])):
            return True

    return False

def most_recent_months(wellness_keys):

    date_pairs = []
    for key in wellness_keys:
        strings = key.split()
        date_pairs.append((int(strings[0]), int(strings[1])))

    dates = sorted(date_pairs, key=lambda x: (x[0], x[1]))
    dates.reverse()

    return_list = []
    for pair in dates[:4]:
        return_list.append(str(pair[0]) + " " + str(pair[1]))

    return return_list
