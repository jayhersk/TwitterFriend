# Main driver code:
# - Creates a directory for the user: '/username/'
# - Gets a list of all of the user's close friends: '/username/username_network.json'
# - For each close friend, scrape all of their data (if it doesn't already exist) and save
#   in: 'username/friend_data/friendname_tweets.json'
# - For each friend, analyze the data, and save the results in 
#   'username/friend_wellness/friendname_wellness.json'
# - Once all friends have been analyzed, make a list of all friends with recent low wellness
#   and save in '/username/friend_alerts.json'

import tweepy #https://github.com/tweepy/tweepy
import json
import sys
import getopt
import os

import get_user_tweets
import get_user_close_friends

def check_input(argv):
    username = ''
    try:
        opts, args = getopt.getopt(argv,"hu:",["uname="])
    except getopt.GetoptError:
        print('main.py -u <username>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -u <username>')
            sys.exit()
        elif opt in ("-u", "--uname"):
            username = arg

    if username == '':
        print('main.py -u <username>')
        sys.exit()

    return username

if __name__ == '__main__':

    username = check_input(sys.argv[1:])

    # Make a directory for this user
    if not os.path.exists(username):
        os.makedirs(username)

    # If we don't have the friend list, get it
    friends_path = os.path.join(username, username + "_network.json")
    if not os.path.exists(friends_path):
        # pass in the username of the account you want to download
        data = get_user_close_friends.get_friends(username)

        # write the json file
        with open(friends_path, 'w') as outfile:
            json.dump(data, outfile, indent=2)

    # Create directories for friend data
    friend_data_path = os.path.join(username, 'friend_data')
    if not os.path.exists(friend_data_path):
        os.makedirs(friend_data_path)

    friend_score_path = os.path.join(username, 'friend_wellness')
    if not os.path.exists(friend_score_path):
        os.makedirs(friend_score_path)

    # Get the list of friends:
    friend_list = []
    with open(friends_path) as network_json:
        data = json.load(network_json)
        friend_list = data['close_friends']

    # For each friend, scrape their tweets and save the data to
    # 'username/friend_data/friendname.json'
    for friendname in friend_list:
        filepath = os.path.join(friend_data_path, friendname + '.json')
        if not os.path.exists(filepath):
            data = get_user_tweets.get_all_tweets(friendname)
            with open(filepath, 'w') as outfile:
                json.dump(data, outfile, indent=2)

    # For each friend, calculate their wellness scores and save the data to
    # 'username/friend_wellness/friendname.json'
    for friend_data_json in os.listdir(friend_data_path):
        pass

    # For each file in friend_wellness, save list to '/username/friend_alerts.json'
    for friend_wellness_json in os.listdir(friend_score_path):
        pass
