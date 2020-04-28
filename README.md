# si660: TwitterFriend 🤖💖
A tool to help you help your friends!
Demo video: https://youtu.be/RBC5JVvvieM

#### Table of Contents  
[Running Website Locally](#run-local)

[Deploying Website to Server](#run-server) 
   
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

### Deploying Website to Server:
<a name="run-server"/>


### Project Description:

In this project, we developed a Chrome extension called “TwitterFriend” that serves as reminders to check in on your friends when they are stressed. Basically, it shows you a list of your friends’ names and their corresponding wellness statuses. If a friend is doing well lately, then his or her wellness status would be “😄 Doing ok! 😄”. On the other hand, if a friend is not doing well lately, then his or her wellness status would be “😰Seems stressed😰” with a red highlight on the text. The motivation behind this project is to encourage users to care about their friends’ wellness and prompt them to reach out to their friends if they are stressed out, given how easy it is to miss out a friend’s content on Twitter because of the algorithm. 

We were originally inspired by the paper “Predicting Depression via Social Media” authored by De Choudhury et al. We thought we could leverage the behavioral cues on social media to build a classifier that provides estimates of the risk of the depression, before the reported onset. However, given the accuracy of the model could not reach 100%, the chance of misclassifying someone’s wellness status could be detrimental. For example, if someone has a risk of depression, but her status shows that she is doing well, then this classification would be considered unethical. Due to this concern, we were looking for an alternative that has less serious consequences on users. We were recommended to read the paper “Modeling Stress with Social Media Around Incidents of Gun Violence on College Campuses” (Saha & De Choudhury), we found that predicting stress might be a good way to go. “Stress is a psychological reaction that occurs when an individual perceives that environmental demands exceed his or her adaptive capacity” (Selye, 1956). Given when we were working on this project, people around the world were dealing with the COVID-19 pandemic, we thought our extension could alleviate the pain induced by the period of extreme social distancing. We use the Vader Sentiment Analysis tool and insomnia index to calculate a user’s wellness score. And we use the basic threshold to classify: if the score is 1 standard deviation below the user’s average and if the score decreases for 5 periods in a row, we classify him as “😰Seems stressed😰”. We hope this extension could help the stressed out people have someone to talk to.
