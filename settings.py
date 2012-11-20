SQLALCHEMY_DATABASE_URI =  'sqlite:////path/to/dropbucket/dev.sqlite'

FACEBOOK_CONSUMER_KEY = ''
FACEBOOK_CONSUMER_SECRET = ''

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

VK_CONSUMER_KEY = ''
VK_CONSUMER_SECRET = ''


try:
    from settings_local import *
except ImportError:
    pass
