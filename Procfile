web: KIRIN_USE_GEVENT=true ./manage.py runserver -p 54746
load_realtime: KIRIN_USE_GEVENT=true ./manage.py load_realtime
worker: celery worker -A kirin.tasks.celery -c 3
scheduler: celery beat -A kirin.tasks.celery
