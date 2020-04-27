"""
TwitterFriend python package configuration.

"""

from setuptools import setup

setup(
    name='TwitterFriend',
    version='0.1.0',
    packages=['TwitterFriend'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'nodeenv',
        'sh',
        'Flask-Testing',
        'selenium',
        'requests',
        'arrow',
        'tweepy'
    ],
)