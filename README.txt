http://127.0.0.1:8000/django-rq/
http://127.0.0.1:8000/admin

python manage.py runserver
python manage.py rqworker --worker-class rq_win.WindowsWorker 