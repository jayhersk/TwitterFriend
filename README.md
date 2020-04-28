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
