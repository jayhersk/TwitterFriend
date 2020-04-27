"""
TwitterFriend development configuration.

"""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b"[EL'\xfe\x0e\xd3\x82\xf0\x99S\x01{\x8f\xfe\t\xf0\xeb\xf4$\xf9\xf8\xefp"  # noqa: E501  pylint: disable=line-too-long
SESSION_COOKIE_NAME = 'TwitterFriend'

# Database file is var/TwitterFriend.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'TwitterFriend.sqlite3'
)

# Twitter Application API Keys:
# Access with TwitterFriend.app.config['API_KEY']
API_KEY = "H47SnDAQB2LZhowA30iYM5R0N"
API_SECRET = "wUCPwf5Ibk26a61ySXehZjWNwZ2C5zDsC2kXHlpHvFPkQKhn3D"