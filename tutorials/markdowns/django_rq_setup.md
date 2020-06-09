There are multiple ways to run a queue in Django. `django-rq` library provides such functionality using *Redis*. 

## Instructions
The setup requires a separate terminal running on a non-Windows platform. Thus a Linux subsystem is used in below setup -- see **Linux Subsystem Setup** page for those instructions. 

1.  `pip install django-rq django-redis-cache`
2.  apply the changes to the files below.
3.  run `python manage.py rqworker` on the linux subsystem
4.  run `python manage.py runserver` from PyCharm
5.  open up browser and navigate to *localhost:8000*
6.  the queue should start, see linux subsystem terminal

### settings.py
Replace the **yourpassword** with your actual password, better to store it in the environment variables.
```python
INSTALLED_APPS = [
...

    # libraries
    'django_rq',
...

# DJANGO-RQ
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'localhost:6379:1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'MAX_ENTRIES': 5000,
        },
    },
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': 'yourpassword',
        'DEFAULT_TIMEOUT': 360,
    },
}
```

### urls.py
```python
urlpatterns = [
...

    path('django-rq/', include('django_rq.urls'))
]
```

### tasks.py
This file defines the tasks that are to placed into the queue. A simple delay timer of 60 seconds is used for testing purposes.
```python
from django_rq import job
import time as t


@job
def timer_queue():
    t.sleep(60)  # sleep 60 seconds
```

### views.py
In the view, the timer queue is called to add to queue. The page loads for the user right away and the task is added to the queue.
```python
import logging

from django.shortcuts import render
from django.http import HttpResponse
from .tasks import timer_queue

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


def index(request):
    # run the queue job
    timer_queue.delay()

    return HttpResponse("Hello logging world.")
```

## Links
[Setup Guide](https://www.imagescape.com/blog/2018/12/21/django-rq-setup-guide/)  
[Pypi django-rq](https://pypi.org/project/django-rq/)  
[Asynchronous django-rq](https://en.proft.me/2016/10/4/asynchronous-tasks-and-jobs-django-rq/)  
[GitHub django-rq](https://github.com/rq/django-rq)  
[connection refused](https://stackoverflow.com/questions/36088409/error-111-connecting-to-localhost6379-connection-refused-django-heroku)  
[connection error](https://stackoverflow.com/questions/44491221/redis-is-running-but-im-getting-error-111-connecting-to-localhost6379-connec)  