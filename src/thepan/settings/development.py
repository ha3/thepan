from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SECRET_KEY = '&_h$3kvn+j0&bal^#@k$kbd*(&w)&prp^68oy08_dvk#d$f+ga'

DEBUG = True

ALLOWED_HOSTS = []
