"""
TwitterFriend package initializer.

"""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (TwitterFriend/config.py)
app.config.from_object('TwitterFriend.config')

# Overlay settings read from file specified by environment variable. This is
# useful for using different on development and production machines.
# Reference: http://flask.pocoo.org/docs/config/
app.config.from_envvar('TWITTERFRIEND_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import TwitterFriend.views  # noqa: E402  pylint: disable=wrong-import-position
import TwitterFriend.model  # noqa: E402  pylint: disable=wrong-import-position
import TwitterFriend.api    # noqa: E402  pylint: disable=wrong-import-position