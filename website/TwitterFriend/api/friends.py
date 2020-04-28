import flask
import datetime
import json
import time
import tweepy

import requests
from flask import request

import TwitterFriend

from TwitterFriend.api.util import forbidden_403
from TwitterFriend.model import model_has_friends_for
from TwitterFriend.model import model_get_friends
from TwitterFriend.model import model_add_friend_list

@TwitterFriend.app.route('/api/friends/', methods=["GET"])
def friend_list():

    # Fancy message for invalid access
    if "username" not in flask.session:
         return forbidden_403()

    # User info:
    logname = flask.session['username']

    # Start return data:
    context = {}
    context["logname"] = logname
    context["url"] = flask.request.path

    # If we don't have friends yet, scrape the data from twitter and put it in the database
    if not model_has_friends_for(logname):

        # get list of friend username/ fullname pairs
        friend_username_list = get_friends(logname)
        model_add_friend_list(logname, friend_username_list)

    # Query database and return friend list
    all_friends = model_get_friends(logname)
    context["friends"] = []
    for friend in all_friends:
        friend["url"] = "/api/f/" + str(friend["fid"]) + "/"
        context["friends"].append(friend)

    return flask.jsonify(**context)

def get_friends(screen_name):

    consumer_key = TwitterFriend.app.config['API_KEY']
    consumer_secret = TwitterFriend.app.config['API_SECRET']
    user_token = flask.session['token']

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(user_token[0], user_token[1])
    api = tweepy.API(auth)

    user_info = api.get_user(screen_name)

    print("Getting user followers...")

    # get followers
    followers = []
    users = tweepy.Cursor(api.followers, screen_name=screen_name, count=200).items()
    while True:
        try:
            user = next(users)
        except tweepy.TweepError:
            print("Reached API limit. Sleeping now.")
            time.sleep(60*15)
            user = next(users)
        except StopIteration:
            break

        # Append username/ fullname pair to list:
        followers.append((user.screen_name, user.name))

    print("Done getting user followers. Total: " + str(len(followers)))
    print("Getting user friends...")

    # get following (also called 'friends')
    friends = []
    users = tweepy.Cursor(api.friends, screen_name=screen_name, count=200).items()
    while True:
        try:
            user = next(users)
        except tweepy.TweepError:
            print("Reached API limit. Sleeping now.")
            time.sleep(60*15)
            user = next(users)
        except StopIteration:
            break

        # Append username/ fullname pair to list:
        friends.append((user.screen_name, user.name))

    print("Done getting user friends. Total: " + str(len(friends)))
    print("Getting close friends...")

    close_friends = list(set(followers) & set(friends))
    print("Done getting user close friends. Total: " + str(len(close_friends)))

    data = {}
    data['close_friends'] = close_friends
    data['followers'] = followers
    data['friends'] = friends

    # Return list of username/ fullname pairs
    return close_friends