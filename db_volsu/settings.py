import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = "f5515c60261d4d29f84e45fbe11f13b1d63495fafe0575be"
DEBUG = True
HEROKU_DEBUG = 1
HEROKU_DEBUG_HEADERS = 1

CACHE_TTL = 60 * 60

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": os.environ.get('REDIS_URL'),
        "LOCATION": "redis://h:p82e6b07ff91254c604c6916a72ad8aa19a689b20640215945ce8f98cc28fbd13@ec2-54-216-126-242.eu-west-1.compute.amazonaws.com:13399",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "conn_params"
    }
}

# SESSION_ENGINE = os.environ.get('SESSION_ENGINE')
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = os.environ.get('SESSION_CACHE_ALIAS')
SESSION_CACHE_ALIAS = "default"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "uranami.pythonanywhere.com", "dbvolsu.herokuapp.com"]
INTERNAL_IPS = ('127.0.0.1', 'localhost', "uranami.pythonanywhere.com", "dbvolsu.herokuapp.com")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
    'db_volsu'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'db_volsu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'db_volsu.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "db_volsu/staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "db_volsu/static"),)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
