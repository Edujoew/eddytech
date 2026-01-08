import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Default to False for safety

# Vercel needs these to communicate with your app
ALLOWED_HOSTS = ['.vercel.app', 'now.sh', 'localhost', '127.0.0.1']

# --- APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # For static files in dev
    'django.contrib.staticfiles',
    'django_daraja', 
    'eddytech',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essential for Vercel
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_website.urls'
WSGI_APPLICATION = 'my_website.wsgi.application'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- STATIC & MEDIA ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise optimization for compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- EMAIL ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER') 
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')

# --- DARAJA / M-PESA ---
MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT', 'sandbox')
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379')
MPESA_EXPRESS_SHORTCODE = os.getenv('MPESA_EXPRESS_SHORTCODE', '174379')
MPESA_SHORTCODE_TYPE = 'paybill'
MPESA_INITIATOR_USERNAME = os.getenv('MPESA_INITIATOR_USERNAME', 'testuser')
MPESA_INITIATOR_SECURITY_CREDENTIAL = os.getenv('MPESA_INITIATOR_SECURITY_CREDENTIAL', 'testpassword')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'