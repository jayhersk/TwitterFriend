# Gets a list of twitter usernames of a user's mutual followers
# Only contains users with public profiles
# Writes the resulting list to a json file (for now)

import tweepy #https://github.com/tweepy/tweepy
import json
import time

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def get_friends(screen_name):

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
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
            time.sleep(60*15)
            user = next(users)
        except StopIteration:
            break
        followers.append(user.screen_name)

    print("Done getting user followers. Total: " + str(len(followers)))
    print("Getting user friends...")

    # get following (also called 'friends')
    friends = []
    users = tweepy.Cursor(api.friends, screen_name=screen_name, count=200).items()
    while True:
        try:
            user = next(users)
        except tweepy.TweepError:
            time.sleep(60*15)
            user = next(users)
        except StopIteration:
            break
        friends.append(user.screen_name)

    print("Done getting user friends. Total: " + str(len(friends)))
    print("Getting close friends...")

    close_friends = list(set(followers) & set(friends))
    print("Done getting user close friends. Total: " + str(len(close_friends)))

    data = {}
    data['close_friends'] = close_friends
    data['followers'] = followers
    data['friends'] = friends

    # write the json file
    with open(screen_name + '_network.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)

if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_friends("jayhersk")