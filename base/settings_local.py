from .settings import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES['default'] = DATABASES['local']
