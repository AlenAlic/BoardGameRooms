import os
from random import choice
from string import ascii_letters
# noinspection PyPackageRequirements
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    ENV = os.environ.get('ENV') or 'production'
    DEBUG = os.environ.get('DEBUG') == "True" or False

    SECRET_KEY = os.environ.get('SECRET_KEY') or ''.join([choice(ascii_letters + '0123456789') for _ in range(64)])

# requirements
# pip freeze > requirements.txt
