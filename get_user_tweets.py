#!/usr/bin/env python
# encoding: utf-8

# SOURCE: https://gist.github.com/brenorb/1ec2afb8d66af850acc294309b9e49ea

# SCRAPES AND CLEANS TWEETS:
# - Gets all tweets from a user and sorts into tweets, retweets, and replies
# - Quote tweets are included in tweets

# Removes all:
# - Punctuation
# - Contractions
# - Mentions and hashtags
# - Emoji and other non-printable characters
# - Links

# Saves result as a json file (for now)

import tweepy #https://github.com/tweepy/tweepy
import json
import re
import string

import contractions

#Twitter API credentials
consumer_key = "uO1tWq8VzLVlpIdv2xIdEZguy"
consumer_secret = "ch6vGSDHroxrD7v6NAmhAmrUOZ6DXgLsot3HZ84grSd0VB4WSc"
access_key = "519923288-jXyVgPgjaRCqEeu6kkfp33pgGB1nG5PUnYt0iDVn"
access_secret = "6QO8xSPSCUE3EiSSHZdbR2X5M5hxLAMbUVTtUQYvAnwbq"

def clean_tweet(text):
	# remove emoji characters/ other unicode characters
	text = ''.join(c for c in text if c in string.printable)

	word_list = text.split()
	new_word_list = []
	for word in word_list:
		# lowercase all
		new_word = word.lower()

		# separate contractions
		if new_word in contractions.CONTRACTIONS.keys():
			new_word_list.append(contractions.CONTRACTIONS[new_word][0])
			new_word_list.append(contractions.CONTRACTIONS[new_word][1])

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

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before {}".format(oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...{} tweets downloaded so far".format(len(alltweets)))

	# PROCESSED JSON OUTPUT:

	# transform tweepy tweets into json
	# alltweets is list of type tweepy.models.Status
	tweets = [] #TODO Still includes some replies (for deleted tweets or private users)
	retweets = []
	replies = []

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

	# write the json file
	with open(screen_name + '_tweets.json', 'w') as outfile:
		json.dump(data, outfile, indent=2)

if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("jayhersk")