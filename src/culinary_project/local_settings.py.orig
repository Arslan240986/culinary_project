import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '80s84g@6^1t)lvt%r-a=f3_fw$^ohfuhgudpa&0bt)j*ju8py1'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'culinary',
        'USER': 'postgres',
        'PASSWORD': '12345qw',
        'HOST': '127.0.0.1',
        'PORT': '5422',
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_project',)
]