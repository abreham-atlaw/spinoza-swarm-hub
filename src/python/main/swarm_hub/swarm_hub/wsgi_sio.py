# myproject/wsgi_socketio.py

import os
import socketio
from django.core.wsgi import get_wsgi_application
from swarm_hub.sio import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swarm_hub.settings")

django_app = get_wsgi_application()

# Wrap Django inside Socket.IO middleware
application = socketio.WSGIApp(sio, django_app)
