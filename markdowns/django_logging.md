Logging capabilities are provided in the `logging` library for python and can be used in django with the following setup.

## Setup
Only requires three files to be edited: views, urls, and settings.

### settings.py
Inside settings, a basic set up would be use `file` and `console` logs. Note that as of June 2020, there is only 1 version for logging.
```python
# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'DEBUG.log',
            'formatter': 'file'
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
    },
}
```

### views.py
To log a message, call the logging instance, e.g. from loading a view.
```python
import logging

from django.http import HttpResponse

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

def index(request):
    # Send the Test!! log message to standard out
    logger.error("Test!!")
    return HttpResponse("Hello logging world.")
```

### urls.py
Set up below to apply the above setup in the urls file
```python
from django.contrib import admin
from django.urls import path, include

from RedisLog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]
```

### Output:
![image](/static/img/markdowns/logging.jpg)

## Links
[documentation](https://docs.djangoproject.com/en/3.0/topics/logging/)  
[tutorial](https://www.scalyr.com/blog/getting-started-quickly-django-logging)  
[another tutorial](https://lincolnloop.com/blog/django-logging-right-way/)  