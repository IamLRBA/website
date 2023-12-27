"""
Django settings for outreachyhome project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import shlex
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',
    'contacts.apps.ContactsConfig',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtail.contrib.table_block',
    'wagtail.contrib.routable_page',

    'modelcluster',
    'taggit',
    'timezone_field',
    'reversion',
    'ckeditor',
    'markdownx',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.forms',
    'betterforms',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'compressor',
    'debug_toolbar',
    'django_extensions',
]

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

MIDDLEWARE = [
    # https://docs.djangoproject.com/en/1.11/ref/middleware/#middleware-ordering
    'outreachyhome.middleware.XForwardedForMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # The documentation says 'You should include the Debug Toolbar middleware
    # as early as possible in the list. However, it must come after any other
    # middleware that encodes the response’s content'
    # I have no idea how to tell which ones handle response content??
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "outreachyhome.debug.show_debug_toolbar",
}

ROOT_URLCONF = 'outreachyhome.urls'

# https://docs.djangoproject.com/en/1.11/ref/forms/renderers/#templatessetting
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.header',
            ],
        },
    },
    {
        # A minimal template configuration for serving "500 Internal
        # Server Error" pages. When things have already gone wrong,
        # try to do as little as possible reporting the problem.
        'NAME': 'errorsafe',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'error-templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                # We need access to the request to get Sentry info for
                # this error.
                'django.template.context_processors.request',
            ],
        },
    },
    {
        'NAME': 'plaintext',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'autoescape': False,
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

# When running under coverage.py, turn on template debugging so
# django_coverage_plugin works.
if sys.gettrace() is not None:
    for engine in TEMPLATES:
        engine['OPTIONS']['debug'] = True

WSGI_APPLICATION = 'outreachyhome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# Update database configuration with $DATABASE_URL.

import dj_database_url  # noqa: E402
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))
}

# In Django 3.2, developers introduced a new way to generate object IDs (pks)
# migrating from the old method (django.db.models.AutoField)
# to the new method (django.db.models.BigAutoField)
# requires us to run an SQL query to change the IDs of all objects in our current database.
# There's no easy way to do that with the current Django migration framework.
#
# https://docs.djangoproject.com/en/3.2/ref/settings/#std-setting-DEFAULT_AUTO_FIELD
#
# For now, tell Django we are explicitly using the old ID generation method.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# If an error occurs in a view, make sure none of that view's changes are saved.
ATOMIC_REQUESTS = True

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(BASE_DIR, 'node_modules', 'd3-timeline-chart', 'dist'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Always use the configured filters, so that browser compatibility hacks
# are applied even in development and we see exactly how the minifiers
# are going to screw up before we bother deploying.
COMPRESS_ENABLED = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',

    # postcss+autoprefixer and clean-css are what Bootstrap uses for
    # their official builds, so hopefully they will work for us too
    'compressor_postcss.PostCSSFilter',
    'compressor.filters.cleancss.CleanCSSFilter',
]

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

COMPRESS_POSTCSS_ARGS = '-c {}'.format(shlex.quote(os.path.join(BASE_DIR, 'postcss.json')))

COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'


# Wagtail settings

WAGTAIL_SITE_NAME = "outreachyhome"
WAGTAILADMIN_BASE_URL = 'https://www.outreachy.org'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'https://www.outreachy.org'
REGISTRATION_OPEN = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# If a new account isn't verified in this many days, don't activate it.
ACCOUNT_ACTIVATION_DAYS = 7

DEFAULT_FROM_EMAIL = 'organizers@outreachy.org'

# Get optional settings for Raven/Sentry error logging. The Sentry DSN
# should be given by the environment variable SENTRY_DSN, which is the
# only environment variable that Raven automatically checks so we don't
# have to pick it up here.
RAVEN_CONFIG = {
    'release': os.getenv('GIT_REV'),
}
