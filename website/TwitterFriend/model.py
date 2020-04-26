"""TwitterFriend model (database) API."""

import sqlite3
import flask
import datetime
import TwitterFriend
import json

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

def user_exists(username):
    """ Check if user exists in database.

        Useful when logging in.
    """
    cursor = get_db().cursor()
    cursor.execute('SELECT uid FROM users WHERE username=?', (username,))
    return len(cursor.fetchall()) == 1