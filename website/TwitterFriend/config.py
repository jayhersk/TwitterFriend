"""
TwitterFriend development configuration.

"""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'Y\xde\x15\xf0!\x04\r\x9elAo\xbb"\xa4!\xe3\xefc\x80Iba\xe62'  # noqa: E501  pylint: disable=line-too-long
SESSION_COOKIE_NAME = 'login'

# Database file is var/TwitterFriend.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'TwitterFriend.sqlite3'
)