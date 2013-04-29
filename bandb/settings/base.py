# Django settings for bandb project.
import os

from .paths import *
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

DEBUG = bool(os.environ.get('DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Steven Day', 'forestorama@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.request",
    "bandb.context_processors.settings"
)

ROOT_URLCONF = 'bandb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bandb.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'bandb', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'pipeline',
    'storages',
    'bandb',
    'bookings'
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
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Email Settings
EMAIL_BACKEND = 'django_ses.SESBackend'

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    # A file-based cache for the hash -> static file mapping
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PROJECT_ROOT, 'static_cache'),
        'TIMEOUT': 100 * 365 * 24 * 60 * 60,  # A hundred years!
        'OPTIONS': {
            'MAX_ENTRIES': 100 * 1000
        }
    },
}

# Site specific settings
# Prices and deposits used in booking process
DEPOSIT = 50
PRICE_PER_NIGHT = 85
PHONE_NUMBER = '01747 854 375'
# Used in emails and templates rather than hardcoding name
SITE_NAME = "Tilley's Hut"
# Used as the from address in emails and on site mailto: links
SITE_EMAIL = 'info@tilleyshut.com'
# Set DEFAULT_FROM_EMAIL and SERVER_EMAIL to SITE_EMAIL too
DEFAULT_FROM_EMAIL = SITE_EMAIL
SERVER_EMAIL = SITE_EMAIL
# People who receive emails about bookings
HOST_BOOKING_RECIPIENTS = [SITE_EMAIL] + [admin[1] for admin in ADMINS]
SITE_BASE_URL = 'http://floating-river-1678.herokuapp.com'

# Secret things parsed from the environment settings
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config(default='postgres://bandb:bandb@localhost:5432/bandb')

# Parse cloudmade api key from local settings
CLOUDMADE_API_KEY = os.environ['CLOUDMADE_API_KEY']

# Parse stripe keys from local settings
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLIC_KEY = os.environ['STRIPE_PUBLIC_KEY']

# Parse AWS settings from local settings
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# FIXME - make keys specifically for SES, not all of AWS
# FIXME - DKIM keys and settings for that
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

AWS_QUERYSTRING_AUTH = False

# Static File things

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/' if DEBUG else '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'web'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage' if DEBUG else 'bandb.lib.S3PipelineStorage'

# Pipeline settings, for compressed/compiled/cached static
# files

PIPELINE_YUGLIFY_BINARY = '/usr/local/bin/yuglify'

PIPELINE_COMPILERS = (
    'pipeline.compilers.sass.SASSCompiler',
)

PIPELINE_SASS_BINARY = '/usr/local/bin/sass'

PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'css/style.scss',
            'css/photoswipe.css'
        ),
        'output_filename': 'css/main.min.css',
        'variant': None,
    }
}

PIPELINE_JS = {
    'main': {
        'source_filenames': (
            'js/lib/klass.min.js',
            'js/lib/code.photoswipe.jquery-3.0.5.min.js',
            'js/lib/moment.min.js',
            'js/gallery.js',
            'js/map.js',
            'js/calendar.js',
        ),
        'output_filename': 'js/main.min.js'
    },
    'icons-lte-ie7': {
        'source_filenames': (
            'js/lib/icons-lte-ie7.js',
        ),
        'output_filename': 'js/lib/icons-lte-ie7.min.js'
    },
    'availability': {
        'source_filenames': (
            'js/availability.js',
        ),
        'output_filename': 'js/availability.min.js'
    },
    'booking': {
        'source_filenames': (
            'js/booking.js',
        ),
        'output_filename': 'js/booking.min.js'
    },
    'payment': {
        'source_filenames': (
            'js/payment.js',
        ),
        'output_filename': 'js/payment.min.js'
    },
}
