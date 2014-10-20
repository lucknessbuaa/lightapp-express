from .settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default'] = DATABASES['local']
