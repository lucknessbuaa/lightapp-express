import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'zuvp4036q9zpc!)0sac=qhk!%udh^5dcavrr@lc6c)m41f3nz%'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']

LOGIN_URL= "/app/login"
LOGIN_ERROR_URL= "/app/login"

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'portal',
    'mgr',
    'backend',
    'social_auth',
    'django_tables2'
)

BAIDU_CLIENT_KEY = 'hqle5S6E74nhq9GVXDiKHG6s'
BAIDU_CLIENT_SECRET = '2G41iSWt01sZpKjHcQwSwdC0bYnbnYAC'
BAIDU_AUTH_EXTRA_ARGUMENTS = {
    'display': 'mobile'
}

WEIBO_CLIENT_KEY = '3384169425'
WEIBO_CLIENT_SECRET = '31f0b9ff71cff9a4e7d70f0784d5a0f5'

QQ_CLIENT_KEY = '101159743'
QQ_CLIENT_SECRET = 'f7297c665355649d36ec6c518f2659f1'

SOCIAL_AUTH_UID_LENGTH = 128
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 128
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 128
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 128

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/app/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/app/'
#SOCIAL_AUTH_RAISE_EXCEPTIONS = True

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.weibo.WeiboBackend',
    'oauth.qq.QQBackend',
    'oauth.baidu.BaiduBackend',
    'django.contrib.auth.backends.ModelBackend'
)

MIDDLEWARE_CLASSES = (
    'base.SocialAuthExceptionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'base.urls'

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
} 
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kWjANFmEFkQdhjctPPIJ',
        'USER': 'xBExZl897GD0mbhICvtT1irv',
        'PASSWORD': '4pNDCphcAYRe4YARIkTO0eokP9pI5hZM',
        'HOST': 'sqld.duapp.com',
        'PORT': '4050'
    },

    'local': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'express',
        'USER': 'root',
        'PASSWORD': 'nameLR9969',
        'HOST': 'localhost',
        'PORT': '3306'
    }, 
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}
'''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

from .loggers import LOGGING
