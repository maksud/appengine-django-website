# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os, sys, re


DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# Activate django-dbindexer for the default database
#DATABASES['native'] = DATABASES['default']
DATABASES['native'] = { 
        'ENGINE': 'djangoappengine.db', 
        'HIGH_REPLICATION': True, 
        'DEV_APPSERVER_OPTIONS': { 
            'high_replication' : True, 
            'use_sqlite': True, 
            } 
    } 
#DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
DATABASES['default'] = DATABASES['native']
AUTOLOAD_SITECONF = 'indexes'

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#    'middlewares.dynamicloader.loader.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'djangotoolbox',
    'autoload',
    'dbindexer',
    'permission_backend_nonrel',
	'uni_form',
    'apps.filetransfers',
    'maxsite',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
#TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates/maxsite')
)

DYN_TEMPLATE_MAP = {
    'HTTP_USER_AGENT': {
        re.compile('iPhone'): (os.path.join(ROOT_PATH,'templates/touch'),)
    }
}

ROOT_URLCONF = 'urls'
