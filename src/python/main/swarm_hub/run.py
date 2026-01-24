# run_gevent_debug.py

# from gevent import monkey
# monkey.patch_all()

import os
import sys
from gevent.pywsgi import WSGIServer
from django.utils.autoreload import run_with_reloader

from swarm_hub.wsgi_sio import application


def main():
    server = WSGIServer(("0.0.0.0", 8000), application)
    print("Starting gevent debug server on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    # Ensure Django settings are set
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swarm_hub.settings")

    # This wraps main() in Django's file-watching reloader
    run_with_reloader(main)
