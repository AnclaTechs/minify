web: gunicorn src/minify/wsgi:application
worker: celery worker -A src/minify --loglevel=info