TEST
http://127.0.0.1:8000/django-rq/
http://127.0.0.1:8000/admin

python manage.py runserver
python manage.py rqworker --worker-class rq_win.WindowsWorker 
python scripts/export-data.py 


To clear Cache
python manage.py shell

>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()


Documentation RST (ReStructured Text)
http://localhost:8000/api/swagger/

CAVE: In dev-Mode on localhost, change frontend and back url in settings.py first
