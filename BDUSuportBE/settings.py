"""
Django settings for BDUSuportBE project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c2z3fdbpliz52-5d=gm=6)=u)4ue=0@s)zcqm=mj=okkrc)=fb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'bduSuport',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BDUSuportBE.urls'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'bduSuport.middlewares.custom_exception_handler.custom_exception_handler'
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'bduSuport.middlewares.custom_jwt_authentication.BackofficeAuthentication'
    # ]
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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



WSGI_APPLICATION = 'BDUSuportBE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_ENGINE = config("DATABASE_ENGINE", "")
DATABASE_NAME = config("DATABASE_NAME", "")
DATABASE_USER = config("DATABASE_USER", "")
DATABASE_PASSWORD = config("DATABASE_PASSWORD", "")
DATABASE_HOST = config("DATABASE_HOST", "")
DATABASE_PORT = config("DATABASE_PORT", 3306)

DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{DATABASE_ENGINE}',
        'NAME': DATABASE_NAME,
        'USER' : DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}

REDIS_HOST = config("REDIS_HOST", "")
REDIS_PORT = config("REDIS_PORT", "")
REDIS_USERNAME = config("REDIS_USERNAME", "")
REDIS_PASSWORD = config("REDIS_PASSWORD", "")

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", 587)  
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = config("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", "")

AUTH_USER_MODEL = 'bduSuport.Account'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',

    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'bduSuport.middlewares.custom_user_authentication_rule.custom_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    'TOKEN_OBTAIN_SERIALIZER': 'bduSuport.serializers.custom_token_obtain_pair_serializer.CustomTokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'bduSuport.serializers.custom_token_refresh_serializer.CustomTokenRefreshSerializer'
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

FIREBASE_CERTIFICATE = config("FIREBASE_CERTIFICATE", "firebase_cert.json")
FIREBASE_STORAGE_BUCKET_URL = config("FIREBASE_STORAGE_BUCKET_URL", "")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    'handlers': {
        'logtail': {
            'class': 'logtail.LogtailHandler',
            'source_token': config("BETTERSTACK_LOG_TOKEN", ""),
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": [
                "logtail",
                "console"
            ],
            "level": "INFO",
        },
    },
}