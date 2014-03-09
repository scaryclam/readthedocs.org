""" Override everything. RTD hardcodes way too much stuff so we need to make
    sure there's nothing left of their very specific config.
"""
from settings.base import *

_ = gettext = lambda s: s


DATABASES = {
}

DEBUG = True
TEMPLATE_DEBUG = True
# We should nuke tasypie
TASTYPIE_FULL_DEBUG = False
CELERY_ALWAYS_EAGER = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

SITE_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
MEDIA_ROOT = '%s/media/' % SITE_ROOT
STATIC_ROOT = os.path.join(SITE_ROOT, 'media/static/')

ADMINS = ()
MANAGERS = ADMINS

DOCROOT = os.path.join(SITE_ROOT, 'user_builds')
UPLOAD_ROOT = os.path.join(SITE_ROOT, 'user_uploads')
CNAME_ROOT = os.path.join(SITE_ROOT, 'cnames')
LOGS_ROOT = os.path.join(SITE_ROOT, 'logs')

# We're going to be smarter than haystack so kill it
HAYSTACK_CONNECTIONS = {
}

# Don't want to use redis
CACHES = {
}

CACHE_MIDDLEWARE_SECONDS = 60

LOGIN_REDIRECT_URL = '/dashboard/'
FORCE_WWW = False

# Elasticsearch settings. Again, kill it
ES_HOSTS = []
ES_DEFAULT_NUM_REPLICAS = 0
ES_DEFAULT_NUM_SHARDS = 0

SLUMBER_API_HOST = ''
WEBSOCKET_HOST = ''

PRODUCTION_DOMAIN = ''
USE_SUBDOMAIN = True
NGINX_X_ACCEL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en', _('English')),
)
LOCALE_PATHS = (
    os.path.join(SITE_ROOT, 'readthedocs', 'locale'),
)

USE_I18N = True
USE_L10N = True
SITE_ID = 1
SECRET_KEY = 'qwb-1908pnq*7gejqfl96$=790c#0le1_p70=koyp0w@f+5a#+'

ACCOUNT_ACTIVATION_DAYS = 7

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'core.middleware.SubdomainMiddleware',
    'core.middleware.SingleVersionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

CORS_ORIGIN_REGEX_WHITELIST = ()
# So people can post to their accounts
CORS_ALLOW_CREDENTIALS = False
ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    '%s/readthedocs/templates/' % SITE_ROOT,
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "core.context_processors.readthedocs_processor",
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # third party apps
    'pagination',
    'registration',
    'profiles',
    'taggit',
    'south',
    'basic.flagging',
    'djangosecure',
    'guardian',
    'django_gravatar',
    'django_nose',
    'rest_framework',
    'corsheaders',

    # Celery bits
    'djcelery',
    'celery_haystack',

    # daniellindsleyrocksdahouse
    'haystack',
    'tastypie',

    # our apps
    'projects',
    'builds',
    'core',
    'rtd_tests',
    'websupport',
    'restapi',
]

REST_FRAMEWORK = {
}

CELERY_ALWAYS_EAGER = True
CELERYD_TASK_TIME_LIMIT = 60 * 60
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_ROUTES = {
}


DEFAULT_FROM_EMAIL = "no-reply@example.com"
SESSION_COOKIE_DOMAIN = ''

AUTH_PROFILE_MODULE = "core.UserProfile"
SOUTH_TESTS_MIGRATE = False

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/profiles/%s/" % o.username
}

INTERNAL_IPS = ('127.0.0.1',)

IMPORT_EXTERNAL_DATA = True

backup_count = 1000
maxBytes = 500 * 100 * 100
if LOG_DEBUG:
    backup_count = 2
    maxBytes = 500 * 100 * 10


# Guardian Settings
GUARDIAN_RAISE_403 = False
ANONYMOUS_USER_ID = -1

# RTD Settings
REPO_LOCK_SECONDS = 30
ALLOW_PRIVATE_REPOS = False

LOG_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
    },
    'handlers': {
    },
    'loggers': {
    }
}

# Ok, now we've cleaned house, we can can actually import a real config
import os

# Use an env variable to determine which settings file to import.  Then copy
# all variables into the local namespace.

# If you want custom settings, create a new settings file (eg conf.barry) and
# import * from conf.local then apply your overrides.
conf_module = os.environ.get('DJANGO_CONF', 'conf.local')
try:
    module = __import__(conf_module, globals(), locals(), ['*'])
except ImportError:
    print "Unable to import %s" % conf_module
else:
    for k in dir(module):
        if not k.startswith("__"):
            locals()[k] = getattr(module, k)
