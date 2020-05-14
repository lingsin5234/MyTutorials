from django.db import models
from datetime import date as dt


# Tutorials
class Tutorial(models.Model):
    name = models.CharField(max_length=50, unique=True)
    filename = models.CharField(max_length=50, unique=True)
    created_on = models.DateField(default=dt.today)

    def __str__(self):
        return str(self.name)
