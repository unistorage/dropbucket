DEBUG = False

CSRF_ENABLED = False

SQLALCHEMY_DATABASE_URI =  'sqlite:////path/to/dropbucket/dev.sqlite'

SECRET_KEY = ''

FACEBOOK_CONSUMER_KEY = ''
FACEBOOK_CONSUMER_SECRET = ''

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

VK_CONSUMER_KEY = ''
VK_CONSUMER_SECRET = ''

UNISTORAGE_URL = ''
UNISTORAGE_ACCESS_TOKEN = ''


try:
    from settings_local import *
except ImportError:
    pass
