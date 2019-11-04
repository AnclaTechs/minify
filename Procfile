web: sh -c 'cd src && gunicorn minify.wsgi'
worker: sh -c 'cd src && celery worker -A minify --loglevel=info'