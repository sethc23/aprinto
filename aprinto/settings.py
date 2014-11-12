from os import path as os_path
from uuid import getnode as get_mac

macs = {'Macbook':'105773427819682',
        'MacBookPro':'117637351435',
        'MBP2':'220083054034723'}

this_mac = get_mac()
if str(this_mac)==macs['MBP2']:
    LOG_DIR = '/Users/admin/SERVER3'
    DB_HOST = '192.168.3.52'
    DB_PORT = '8800'
else:
    LOG_DIR = '/home/ec2-user/SERVER4'
    DB_HOST = '0.0.0.0'
    DB_PORT = '8800'

BASE_DIR = os_path.dirname(os_path.dirname(__file__))
BASE_APP_URL = 'http://app.aporodelivery.com/'
BASE_PRINTER_URL = 'http://printer.aporodelivery.com/'
BASE_QR_URL = BASE_APP_URL + 'qr/'
# INCL_CHARS = set('ACEFGHJKLNPSTXZ347')
INCL_CHARS = 'ACEFGHJKLNPSTXZ347'
INCL_CHARS_LEN = len(INCL_CHARS)
FWD_ORDER = False
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%6d$oxj6)29$o$^jr)fav8j^sey-&2(gcofj*lk^j%bg#rpci)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'app',
    # 'pdf',
    'aprinto',
    # 'ghettoq',
    # 'djcelery',
    # 'djcelery.transport',
    # 'kombu',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aprinto.urls'
WSGI_APPLICATION = 'aprinto.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aprinto',
        'USER': 'postgres',
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'client_encoding': 'UTF8'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False       # If you set this to False, Django will not use timezone-aware datetimes.


# Static files (CSS, JavaScript, Images)
PROJECT_ROOT = os_path.dirname(os_path.dirname(__file__))
STATIC_ROOT = os_path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os_path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
PDF_UPLOAD_PATH = os_path.join(PROJECT_ROOT, 'uploads')

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
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            #'filename': LOG_DIR + '/run/logs/django/console.log',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/run/logs/django/filehandler.log',
            'maxBytes': 1024000,
            'backupCount': 3,
        },
        'sql': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/run/logs/django/sql.log',
            'maxBytes': 102400,
            'backupCount': 3,
        },
        'commands': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/run/logs/django/commands.log',
            'maxBytes': 10240,
            'backupCount': 3,
        },
        'mail_admins': {
            'level': 'ERROR',
            #'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
       'django': {
            'handlers': ['file', 'console','mail_admins',],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['sql', 'console'],
            'propagate': False,
            'level': 'WARNING',
        },
        'scheduling': {
            'handlers': ['commands', 'console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['file', 'console', 'mail_admins',],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# REDIS/CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json','pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny'
    ]
}