import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '80s84g@6^1t)lvtshvdjejckab663384bbcj8ba)fuhgudpa&0bt)j*ju8py1'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '5.101.5.119', 'ushefa.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ushefa',
        'USER': 'arslan_chef',
        'PASSWORD': 'arslan240986',
        'HOST': '127.0.0.1',
        'PORT': '5422',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'culinary',
#         'USER': 'postgres',
#         'PASSWORD': '12345qw',
#         'HOST': '127.0.0.1',
#         'PORT': '5422',
#     }
# }
# if DEBUG:
#     STATIC_DIR = os.path.join(BASE_DIR, 'static')
#     STATICFILES_DIRS = [
#         STATIC_DIR,
#     ]
# else:
#     STATICFILES_DIRS = [
#         os.path.join(BASE_DIR, 'static'),
#     ]
#     STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn/', 'static_root/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static',)
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn', 'static_root')