from os import path as os_path
BASE_DIR = os_path.dirname(os_path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%6d$oxj6)29$o$^jr)fav8j^sey-&2(gcofj*lk^j%bg#rpci)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'pdf',
    'celery',
    # 'ghettoq',
    'djcelery',
    'djcelery.transport',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aprinto.urls'

WSGI_APPLICATION = 'aprinto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aprinto',
        'USER': 'root',
        'PASSWORD': 'Delivery100%',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
PROJECT_ROOT = os_path.dirname(os_path.dirname(__file__))
STATIC_ROOT = os_path.join(PROJECT_ROOT, 'static/')
STATIC_URL = '/static/'

PROJECT_ROOT = os_path.dirname(os_path.dirname(__file__))
STATIC_ROOT = os_path.join(PROJECT_ROOT, 'static/')

MEDIA_ROOT = os_path.join(PROJECT_ROOT, 'media/')
MEDIA_URL = '/media/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    os_path.join(PROJECT_ROOT, 'templates/'), #project-wide templates
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# pdf app settings
PDF_UPLOAD_BUCKET = os_path.join(PROJECT_ROOT, 'uploads/')       # Where the documents should be uploaded to
PDF_AWS_KEY = 'AKIAIW4C3IJB7JJ6WMKQ'             # AWS Key for accessing Bootstrap Bucket and Queues
PDF_AWS_SECRET = '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'          # AWS Secret Key for accessing Bootstrap Bucket and Queues

CARROT_BACKEND = "ghettoq.taproot.Database"
CELERY_RESULT_BACKEND = "amqp"