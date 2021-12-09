from datetime import datetime
from pathlib import Path
import os

import environ


BASE_DIR = Path(__file__).resolve().parent.parent

environ.Path(BASE_DIR / ".env")
ENV = environ.Env()
environ.Env.read_env()


SECRET_KEY = ENV.str('SECRET_KEY')
DEBUG = bool(ENV.str('DEBUG'))

import sys

sys.modules['fontawesome_free'] = __import__('fontawesome-free')

INSTALLED_APPS = [
    'authorization',
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_email_confirmation',
    'social_django',
    'fontawesome_free',
    'django_celery_beat',
    'django_middleware_global_request',
    'main',
    'course',
    'misc',
    'payment',
    'toolbox',
    'help_sessions',
    'login_sessions',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_middleware_global_request.middleware.GlobalRequestMiddleware',
    'authorization.middlewares.email_checker',
    'login_sessions.middleware.OneSessionPerUserMiddleware',
]

ROOT_URLCONF = 'armstrong.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'armstrong.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ENV.str('DB_NAME'),
        'USER': ENV.str('DB_USER'),
        'PASSWORD': ENV.str('DB_PASSWORD'),
        'HOST': ENV.str('DB_HOST'),
        'PORT': ENV.str('DB_PORT'),
    }
}



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


STATICFILES_DIRS= [os.path.join(BASE_DIR, 'main_static')]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
X_FRAME_OPTIONS='SAMEORIGIN'

AUTH_USER_MODEL = 'authorization.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/authorization/login/'

EMAIL_HOST_USER = FROM_EMAIL = ENV.str('EMAIL_HOST_USER')

SOCIAL_AUTH_JSONFIELD_ENABLED = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'authorization.social_pipeline.add_dummy_password',
)
SOCIAL_AUTH_URL_NAMESPACE = 'authorization:social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ENV.str('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ENV.str('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_FACEBOOK_KEY = ENV.str('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = ENV.str('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'email'
}

API_VIDEO_KEY = ENV.str('API_VIDEO_KEY')

CELERY_BROKER_URL = ENV.str('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = ENV.str('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = "Africa/Cairo"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
PAYMOB_API_KEY = ENV.str('PAYMOB_API_KEY')

BOSTA_API_KEY = ENV.str('BOSTA_API_KEY')
BOSTA_USERNAME = ENV.str('BOSTA_USERNAME')
BOSTA_NUMBER = ENV.str('BOSTA_NUMBER')
BOSTA_EMAIL = ENV.str('BOSTA_EMAIL')

AS_LANG = ENV.str('AS_LANG')

URL = ENV.str('URL')

GEOIP_PATH = os.path.join(BASE_DIR, 'payment')
CRYPT_KEY = ENV.str('CRYPT_KEY')
