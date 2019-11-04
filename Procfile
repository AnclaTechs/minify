web: gunicorn src/minify/wsgi.py
worker: celery worker -A src/minify --loglevel=info