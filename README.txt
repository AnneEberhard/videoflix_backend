http://127.0.0.1:8000/django-rq/
http://127.0.0.1:8000/admin

python manage.py runserver
python manage.py rqworker --worker-class rq_win.WindowsWorker 
python export-data.py


To clear Cache
python manage.py shell

>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()


Documentation RST (ReStructured Text)
http://localhost:8000/api/swagger/

https://stackoverflow.com/questions/51462317/django-admin-change-user-password