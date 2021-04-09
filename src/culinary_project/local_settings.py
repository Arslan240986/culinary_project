import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '80s84g@6^1t)lvt%r-a=f3_fw$^ohfuhgudpa&0bt)j*ju8py1'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_project',)
]