from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

AUTH_PASSWORD_VALIDATORS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dev_waiphieQu5Dae2zahzohd9Sai9vaiyushahho1xe2Eif9auteeleingaiyai8ooy'

SOCIAL_AUTH_RAISE_EXCEPTIONS = False

try:
    from .local import *
except ImportError:
    pass
