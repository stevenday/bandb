# Django settings for bandb project.
import os
from datetime import date, timedelta

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

import dj_database_url

from .paths import *

DEBUG = bool(os.environ.get('DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Steven Day', 'forestorama@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                       # Or path to database file if using sqlite3.
        'USER': '',                       # Not used with sqlite3.
        'PASSWORD': '',                   # Not used with sqlite3.
        'HOST': '',                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                       # Set to empty string for default. Not used with sqlite3.
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
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'bookings.middleware.SSLifyMiddleware',
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
    # Long cache timeout for staticfiles, since this is used heavily by the optimizing storage.
    "staticfiles": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "TIMEOUT": 60 * 60 * 24 * 365,
        "LOCATION": os.path.join(PROJECT_ROOT, 'static_cache'),
    },
}

# Secret things parsed from the environment settings
# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config(default='postgres://bandb:bandb@localhost:5432/bandb')

# Parse cloudmade api key from local settings
CLOUDMADE_API_KEY = os.environ['CLOUDMADE_API_KEY']

# AWS settings
# Standard AWS stuff goes here, site-specific stuff is in site.py
AWS_QUERYSTRING_AUTH = False

# Expires set to one year from now, it could be more, ideally ten,
# but max-age fails when you go to ten, with no helpful error, so
# I've stuck to one year for both
one_year = date.today() + timedelta(days=365)
AWS_HEADERS = {
    'Expires': one_year.strftime('%a, %d %b %Y 20:00:00 GMT'),
    'Cache-Control': 'public, max-age=31536000',
}
AWS_PRELOAD_METADATA = True

# Static File things

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# STATIC_URL set in site.py because it relies on site-specific AWS_BUCKET_NAME

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'web'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage' if DEBUG else 'bandb.lib.S3PipelineStorage'

# Pipeline settings, for compressed/compiled/cached static
# files
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

PIPELINE_YUGLIFY_BINARY = '/usr/local/bin/yuglify'

PIPELINE_COMPILERS = (
    'pipeline.compilers.sass.SASSCompiler',
)

PIPELINE_SASS_BINARY = '/usr/local/bin/sass'

PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'css/photoswipe.css',
            'css/style.scss',
        ),
        'output_filename': 'css/main.min.css',
    }
}

PIPELINE_JS = {
    'main': {
        'source_filenames': (
            'js/lib/klass.js',
            'js/lib/code.photoswipe.jquery-3.0.5.js',
            'js/lib/moment.js',
            'js/gallery.js',
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
    'map': {
        'source_filenames': (
            'js/map.js',
        ),
        'output_filename': 'js/map.min.js'
    },
}

PIPELINE_DISABLE_WRAPPER = True

URLS_TO_SSLIFY = (
    'payment',
)

# Import site specific settings
from .site import *
