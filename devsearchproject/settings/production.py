from os import getenv
import cloudinary
import cloudinary_storage
import django_heroku
from .base import *

DEBUG = True

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': getenv('CLOUD_NAME'),
    'API_KEY': getenv('API_KEY'),
    'API_SECRET': getenv('API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = '/devsearch-images/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'devsearchproject@gmail.com'
EMAIL_HOST_PASSWORD = 'zqewufelhmqijbfc'

django_heroku.settings(locals())