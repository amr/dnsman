# Django settings for dnsman project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'database/dnsman.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Cairo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '470u^v!*a1!62^kpzlzsivs4eb=w(2t$+716k%-5cio161@710'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'dnsman.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'templates',
)

INSTALLED_APPS = (
    # Django's default
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Admin
    'django.contrib.admin',

    # DNSMan
    'dnsman.domains',
    'dnsman.redirections',
    'dnsman.parking',
    'dnsman.docs',
)

# Parking pages directory, MUST be relative to MEDIA_ROOT
PARKING_PAGES_DIR = MEDIA_ROOT + '/parking-pages'

# Enable django-varnish, see VARNISH.txt for details
VARNISH_INTEGRATION = False

try:
    from local_settings import *
except ImportError:
    pass

if VARNISH_INTEGRATION:
    INSTALLED_APPS += ('varnishapp', 'django.contrib.humanize')
    MIDDLEWARE_CLASSES += ('dnsman.varnish_integration.middleware.VarnishIntegrationMiddleware',)
    # Each of those models must define varnish_purge_hash_pattern()
    VARNISH_WATCHED_MODELS = ('domains.Domain', 'redirections.Redirection')
    VARNISH_MANAGEMENT_ADDRS = ('127.0.0.1:6082',)

# django-devserver
if DEBUG:
    try:
        import devserver
        INSTALLED_APPS += ('devserver',)
        
        DEVSERVER_MODULES = (
            'devserver.modules.ajax.AjaxDumpModule',
        )
    except ImportError:
        pass
