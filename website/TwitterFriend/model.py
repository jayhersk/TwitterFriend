"""TwitterFriend model (database) API."""

import sqlite3
import flask
import datetime
import TwitterFriend
import json

######################################################

def dict_factory(cursor, row):
    """
    Convert database row objects to a dictionary.

    This is useful for building dictionaries which
    are then used to render a template.  Note that
    this would be inefficient for large queries.
    """
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output

def get_db():
    """Open a new database connection."""
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(
            TwitterFriend.app.config['DATABASE_FILENAME'])
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db

@TwitterFriend.app.teardown_appcontext
def close_db(error):
    # pylint: disable=unused-argument
    """Close the database at the end of a request."""
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()

######################################################

def model_login_user(username, fullname, credentials):
    """ Robust login function. 
        Credentials is a pair structred as (token, token_secret)
    """

    cursor = get_db().cursor()
    if user_exists(username):
        # Update fullname, tokens in DB
        cursor.execute('UPDATE users SET token=?, token_secret=?, \
                            fullname=? WHERE username=?', 
                            (credentials[0], credentials[1], fullname, username)
                      )
        return False

    else:
        # Create User account in DB
        cursor.execute('INSERT INTO users(username, fullname, token, token_secret)\
                        VALUES (?, ?, ?, ?)',
                        (username, fullname, credentials[0], credentials[1])
                      )
        return True # first login

    return

######################################################
## USER DATABASE FUNCTIONS:

def user_exists(username):
    """ Check if user exists in database.

        Useful when logging in.
    """
    cursor = get_db().cursor()
    cursor.execute('SELECT uid FROM users WHERE username=?', (username,))
    return len(cursor.fetchall()) == 1

######################################################
## FRIEND LIST DATABASE FUNCTIONS:

def model_has_friends_for(username):
    """ Check if we have the list of friends for a given user """
    cursor = get_db().cursor()
    cursor.execute('SELECT num_friends FROM users WHERE username=?', (username,))
    response = cursor.fetchone()
    if response == None:
        return False
    return response['num_friends'] != None

def model_get_friends(username):
    """ Return the list of friends from the database """
    cursor = get_db().cursor()
    cursor.execute('SELECT fid, f_username, f_fullname, stressed, checked \
                    FROM user_friends WHERE username=?', (username,))
    return cursor.fetchall()

def model_add_friend_list(username, f_username_list):
    """ Given a username and list of friend username/ fullname PAIRS, add
        all as database entries.
    """
    cursor = get_db().cursor()
    cursor.execute('SELECT uid FROM users WHERE username=?', (username,))

    uid = cursor.fetchone()['uid']

    for pair in f_username_list:
        model_add_friend(username, uid, pair[0], pair[1])


    cursor.execute('UPDATE users SET num_friends=? WHERE username=?', 
                   (len(f_username_list), username))

    return

def model_add_friend(username, uid, friend_username, friend_fullname):
    """ Add a friend into the database (if it doesn't already exist) """
    cursor = get_db().cursor()
    cursor.execute('INSERT INTO user_friends (f_username, f_fullname, username, uid) VALUES (?,?,?,?)', 
                   (friend_username, friend_fullname, username, uid))
    return

def model_get_friend_data(username, fid):
    """Get all data for one friend"""
    cursor = get_db().cursor()
    cursor.execute('SELECT f_username, f_fullname, stressed, checked \
                    FROM user_friends WHERE username=? AND fid=?', (username, fid))
    return cursor.fetchone()

def model_does_friend_need_update(username, fid):
    cursor = get_db().cursor()
    cursor.execute('SELECT f_username, f_fullname, stressed, checked \
                    FROM user_friends WHERE username=? AND fid=?', (username, fid))

    data = cursor.fetchone()
    if data['stressed'] == None:
        return True
    elif data['checked'] != None:
        checked_time = datetime.datetime.strptime(data['checked'], '%Y-%m-%d %H:%M:%S.%f')
        time_diff = datetime.datetime.now() - checked_time
        if time_diff.days > 7:
            return True
        else:
            return False
    return False

######################################################
## FRIEND DATA DATABASE FUNCTIONS

def model_has_friend_scores(fid):
    cursor = get_db().cursor()
    cursor.execute('SELECT month_name FROM scores WHERE fid=?', (fid,))
    return len(cursor.fetchall()) >= 1

def model_set_friend_stress(fid, stressed, checked):
    cursor = get_db().cursor()
    cursor.execute('UPDATE user_friends SET stressed=?, checked=? WHERE fid=?', 
                   (stressed, checked, fid))

    return

def model_save_wellness_scores(fid, wellness_scores):
    cursor = get_db().cursor()
    for key in wellness_scores.keys():

        cursor.execute('SELECT score FROM scores WHERE fid=? AND month_name=?', (fid, key))
        if cursor.fetchone():
            cursor.execute('UPDATE scores SET score=? WHERE fid=? AND month_name=?', (wellness_scores[key], fid, key))
        else:
            cursor.execute('INSERT INTO scores (fid, month_name, score) VALUES (?,?,?)', (fid, key, wellness_scores[key]))
    return

def model_get_wellness_scores(fid):
    cursor = get_db().cursor()
    cursor.execute('SELECT month_name, score FROM scores WHERE fid=?', (fid,))
    data = cursor.fetchall()

    score_dict = {}
    for item in data:
        score_dict[data['month_name']] = data['score']

    return score_dict