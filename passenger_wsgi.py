# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u2922548/data/www/tapca.ru/tapcaproject')
sys.path.insert(1, '/var/www/u2922548/data/venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tapca.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()