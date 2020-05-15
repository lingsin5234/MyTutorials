The most important thing to note is that the migrations need to be run **ONE DATABASE** at a time!

## Instructions
1.  Set up the files as listed below.
2.  Run 'python manage.py migrate --database=default` to send all other apps to default.
3.  Run 'python manage.py migrate --database=[app_db]` for your app(s) with their own database(s).

### routers.py
Create this script in your app folder (e.g. groceryapp). `grocery_db` should match the db ref in settings.py
```python
class GroceryRouter:
    """
    A router to control all database operations
    on models in the grocery app
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'groceryapp':
            return 'grocery_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'groceryapp':
            return 'grocery_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if a model is in the groceryapp
        if obj1._meta.app_label == 'groceryapp' or obj2._meta.app_label == 'groceryapp':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'groceryapp' and db == 'grocery_db':
            # this catches groceryapp for grocery_db ONLY
            return db == 'grocery_db'
        elif app_label == 'groceryapp' or db == 'grocery_db':
            # this catches all that should not be in grocery_db
            # and for groceryapp to not be added to default db
            return False
        # allows other apps to go to default database
        return None
```

### settings.py
Add the database information
```python
# DATABASE ROUTER
DATABASE_ROUTERS = ['groceryapp.routers.GroceryRouter']
DATABASE_APPS_MAPPING = {'groceryapp': 'grocery_db'}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'grocery_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'grocery_db.sqlite3'),
    }
}
```

### models.py
For each of your models in your app, add the app_label to ensure it is read as part of that app.
```python
class Product(models.Model):
    name = models.CharField(max_length=50)
    ...

    class Meta:
        app_label = 'groceryapp'
    
    def __str__(self):
    ...
```

## Other Links
[Main Doc](https://docs.djangoproject.com/en/3.0/topics/db/multi-db/)
[Tutorial](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/multiple_databases.html)
[Tutorial2](https://www.webforefront.com/django/modelmultidatabases.html)  
[Django & SQLAlchemy](https://medium.com/@hariwin7/connecting-to-multiple-databases-dynamically-with-django-and-sqlalchemy-1b0b7454eb3e)  