import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '80s84g@6^1t)lvtshvdjejckab663384bbcj8ba)fuhgudpa&0bt)j*ju8py1'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '146.185.235.119', 'ushefa.ru', 'localhost']
if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'ushefa_ru',
            'USER': 'ushefa_ars',
            'PASSWORD': 'arslan240986',
            'HOST': '127.0.0.1',
            'PORT': '5422',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'culinary_rewrite',
            'USER': 'postgres',
            'PASSWORD': '12345qw',
            'HOST': '127.0.0.1',
            'PORT': '5422',
        }
    }

