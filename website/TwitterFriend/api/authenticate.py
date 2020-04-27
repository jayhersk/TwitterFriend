import json
import tweepy

import flask
import requests
from flask import request

import TwitterFriend
from TwitterFriend.model import model_login_user

@TwitterFriend.app.route('/api/login/')
def api_login():
    """ Initiate Twitter oauth login process. """

    # redirect user if already logged in
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))

    # Get keys
    consumer_key = TwitterFriend.app.config['API_KEY']
    consumer_secret = TwitterFriend.app.config['API_SECRET']

    # create auth handler and pass callback url
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, flask.url_for('api_oauth_callback', _external=True))
    url = auth.get_authorization_url()
    flask.session['request_token'] = auth.request_token

    # redirect user to Twitter for authentication
    return flask.redirect(url)

@TwitterFriend.app.route('/api/oauth_callback')
def api_oauth_callback():
    """ Process google callback url.
        After authenticating user is redirected to this url
        and it extracts the credentials from query string (?asdf=asdf).
    """

    # redirect user if already logged in
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))

    # Get login request token
    request_token = flask.session['request_token']
    # del flask.session['request_token']

    # Get keys
    consumer_key = TwitterFriend.app.config['API_KEY']
    consumer_secret = TwitterFriend.app.config['API_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, flask.url_for('api_oauth_callback', _external=True))
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)

    # Save access tokens
    user_token = (auth.access_token, auth.access_token_secret)
    flask.session['token'] = user_token

    # Query api for user info
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, flask.url_for('api_oauth_callback', _external=True))
    auth.set_access_token(user_token[0], user_token[1])
    api = tweepy.API(auth)
    user = api.me()

    flask.session['username'] = user.screen_name
    flask.session['fullname'] = user.name

    # store/update profile in database
    flask.session["first_login"] = model_login_user(flask.session['username'], 
                                                    flask.session['fullname'], user_token)

    flask.session.modified = True

    if flask.session["first_login"]:
        pass

    # Authentication process complete!
    # get token from database using username stored in session
    return flask.redirect(flask.url_for('show_index'))


def logout():
    """ Logout user. 
        Users are considered logged in if 'username' is in session.
    """
    # pop username from session to 'log' user out
    if 'username' in flask.session:
        flask.session.pop('username')
    return

@TwitterFriend.app.route('/api/logout/')
def api_logout():
    """ Endpoint for standard logout. """

    # redirect to index if user is logged out
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_index'))

    logout()

    return flask.redirect(flask.url_for('show_index'))
