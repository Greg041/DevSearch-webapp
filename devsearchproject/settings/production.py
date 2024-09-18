import cloudinary
import os
from .base import *
from dotenv import load_dotenv

local_env_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(local_env_file):
    load_dotenv(local_env_file)
    
SECRET_KEY = os.getenv('SECRET_KEY')

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