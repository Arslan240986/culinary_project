import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '80s84g@6^1t)lvtshvdjejckab663384bbcj8ba)fuhgudpa&0bt)j*ju8py1'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'culinary',
        'USER': 'arslanUSh',
        'PASSWORD': 'arslan240986',
        'HOST': '127.0.0.1',
        'PORT': '5422',
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_project',)
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'static_root')