from os import getenv
import cloudinary
import cloudinary_storage
import django_heroku
from .base import *

DEBUG = False

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': getenv('CLOUD_NAME'),
    'API_KEY': getenv('API_KEY'),
    'API_SECRET': getenv('API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


MEDIA_URL = '/devsearch-images/'

django_heroku.settings(locals())