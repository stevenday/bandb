"""Site specific settings"""
# TODO - a lot of these should come from the DB, but how will we do the AWS
# Buckets and so on??
import os
import calendar
from datetime import date

DEBUG = bool(os.environ.get('DEBUG', ''))

# Prices and deposits used in booking process
DEPOSIT = 50
PRICE_PER_NIGHT = 85

PHONE_NUMBER = '01747854375'

# Used in emails and templates rather than hardcoding name
SITE_NAME = "Tilley's Hut"

# Used as the from address in emails and on site mailto: links
SITE_EMAIL = 'info@tilleyshut.com'

# Set DEFAULT_FROM_EMAIL and SERVER_EMAIL to SITE_EMAIL too
DEFAULT_FROM_EMAIL = SITE_EMAIL
SERVER_EMAIL = SITE_EMAIL

# People who receive emails about bookings
HOST_BOOKING_RECIPIENTS = [SITE_EMAIL] + ['forestorama@gmail.com']

# We need this to make absolute links in emails and do redirects properly
SITE_BASE_URL = 'http://localhost:5000' if DEBUG else 'http://tilleyshut.herokuapp.com'

# This is used to specify explicitly when linking to the payment page
# so that we can freeload off Heroku's https cert, rather than paying
# $20 a month to be allowed to use our own with our custom domain
HTTPS_URL = 'http://localhost:5000' if DEBUG else 'https://tilleyshut.herokuapp.com'

# Nights of the week we're not available by default
# Used by the bookings app to know which days to hide on the calendar
# These are really just integers from 0 -> 6 as per Calendar's day numbering
DEFAULT_HOLIDAY_NIGHTS = (
    calendar.MONDAY,
    calendar.TUESDAY,
    calendar.WEDNESDAY,
    calendar.THURSDAY
)

# Exceptions to the days above which *will* be available even if they would
# not normally, eg: Bank holiday Mondays
# TODO - Make this a model and let people edit it?
HOLIDAY_EXCEPTIONS = (
    date(2014, 04, 21),  # Easter Monday
    date(2014, 5, 5),  # Early May bank holiday
    date(2014, 5, 26),  # Spring bank holiday
    date(2014, 8, 25),  # Summer bank holiday
    date(2015, 4, 6),  # Easter Monday
    date(2015, 5, 4),  # Early May bank holiday
    date(2015, 5, 5),  # Spring bank holiday
    date(2015, 8, 31),  # Summer bank holiday
)

# Parse stripe keys from local settings
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLIC_KEY = os.environ['STRIPE_PUBLIC_KEY']

# Parse AWS settings from local settings
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# FIXME - make keys specifically for SES, not all of AWS
# FIXME - DKIM keys and settings for that
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

# URL prefix for static files.
STATIC_URL = '/static/' if DEBUG else '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
