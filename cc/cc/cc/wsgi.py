"""
WSGI config for cc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to the sys.path
path = Path(__file__).resolve().parent.parent
sys.path.append(str(path))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cc.settings')

application = get_wsgi_application()
