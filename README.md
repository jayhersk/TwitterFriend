# si660: TwitterFriend 🤖💖
Developing a computational agent that helps you take care of your friends’ mental health

Demo video: https://youtu.be/RBC5JVvvieM

Live Website: http://twitter-friend.jayl.in/

### Table of Contents
[Project Motivation](#motiv)

[Wellness Scores](#well)

[Interface Description](#desc)

[Experimental Features](#exp)

[Running Website Locally](#run-local)
   
### Project Motivation:
<a name="motiv"/>

In this project, we developed a website that serves as a reminder to take care of your friends by monitoring your friends’ mental state by analyzing their post sentiment and other behavioral cues on social media. It's easy to miss out a friend’s content on Twitter because of the volume of content and algorithmic filtering, instead, a bot can monitor them and prompt the user to provide social or emotional support if needed. This project was inspired by the paper “Predicting Depression via Social Media” authored by De Choudhury et al. De Choudhury et al. identify features of a user's Twitter profile and use them to create a classifier to predict if someone has been diagnosed with clinical depression within the past year, before the reported onset.

Additionally, motivated by the paper “Modeling Stress with Social Media Around Incidents of Gun Violence on College Campuses” (Saha & De Choudhury), we thought that detecting stress might be a good alternative. Stress is defined as “a psychological reaction that occurs when an individual perceives that environmental demands exceed his or her adaptive capacity” (Selye, 1956). Given the current global COVID-19 pandemic, we hope our project could help alleviate the stress induced by the period of extreme social distancing.

### Wellness Scores:
<a name="well"/>

Given issues around the pracicality of implemeting the same classifier (unable to get labeled training data, not wanting to classify medical depression without user consent), we repurpose some of the features from De Choudhury et al.'s paper to create a more general 'wellness score' for a user:

1. The sentiment of their Tweets (positive, neutral, or negative), which we identify using `vaderSentiment`.
2. The amount that a user Tweets in the middle of the night (the 'insomnia index').
3. How often Tweet content containins terms that are commonly associated with stress and insomnia. We curate a list of terms based on data scraped from /r/insomnia and /r/stress, from this repository: https://github.com/willisc92/Twitter_sleep_stress.

We perform the above three analysis on a user's Tweets, Retweets,and Replies, then perform a weighted average of the resulting scores. The final score will always be between 0 and 1, and higher scores indicate higher stress levels. We then classify a user as stressed if they meet one of two conditions:

1. If the wellness score for the most recent active month is higher than 0.2 standard deviations above the average wellness score for all active months.
2. If the wellness score has continuously increased for the previous four active months.

### Experimental Features:
<a name="exp"/>

The file `command line tool/analyze_user_wellness.ipynb` also contains additional code to classify a month as 'stressed' or 'not stressed'. More documentation is included in the file.

The rest of the folder `command line tool` contains a protoype command line version of the twitter scraping and analysis code.

### Running Website Locally:
<a name="run-local"/>

1. Set up python virtual environment in website directory
```
python3 -m venv env
source env/bin/activate
```

2. Install utilities
```
pip install --upgrade pip setuptools wheel
pip install Flask
brew install sqlite3 curl httpie coreutils
```

3. Install server-side Python app
```
pip install -e .
```

4. Run bash scripts to launch development server (making them executable if needed)
```
chmod 755 TwitterFriendDB
chmod 755 TwitterFriendRun

bin/TwitterFriendDB create
bin/TwitterFriendRun
```

### Interface Description:
<a name="desc"/>

A full demo video can be found at this link: https://youtu.be/RBC5JVvvieM

Our website “TwitterFriend” that serves as a reminder to check in on your friends when they are stressed. First, a user logs 
in with their Twitter account:

![Login](https://github.com/jayhersk/si660/blob/master/demo%20and%20screenshots/01_loginScreen.png?raw=true)
![Auth](https://github.com/jayhersk/si660/blob/master/demo%20and%20screenshots/02_authorizeTwitter.png?raw=true)

Once a user is logged in, they start pulling their list of mutual Twitter followers and processing their data.

![Start](https://github.com/jayhersk/si660/blob/master/demo%20and%20screenshots/03_startScreen.png?raw=true)
![Load](https://github.com/jayhersk/si660/blob/master/demo%20and%20screenshots/04_getFriendList.png?raw=true)
![Loading](https://github.com/jayhersk/si660/blob/master/demo%20and%20screenshots/05_loadingFriendTweets.png?raw=true)

Finally, the user's friends are classified as stressed or not stressed based on their wellness scores.

![Scores](https://github.com/jayhersk/si660/blob/master/demo%20and%20screenshots/06_classifyFriends.png?raw=true)
