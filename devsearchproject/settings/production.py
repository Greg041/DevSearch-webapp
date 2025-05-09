import cloudinary
import os
from .base import *
from dotenv import load_dotenv


local_env_file = os.path.join(BASE_DIR, f".env/.env.{os.getenv('APP_ENV')}")
if os.path.isfile(local_env_file):
    load_dotenv(local_env_file)

SECRET_KEY = getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', '') != 'False'

cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('CLOUD_API_KEY'),
    api_secret = os.getenv('CLOUD_API_SECRET')
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}