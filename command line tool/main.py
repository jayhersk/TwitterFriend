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
        data = get_user_close_friends.get_friends("jayhersk")

        # write the json file
        with open(friends_path, 'w') as outfile:
            json.dump(data, outfile, indent=2)

    # Create directories for friend data
