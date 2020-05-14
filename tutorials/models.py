from django.db import models
from datetime import date as dt


# Tutorials
class Tutorial(models.Model):
    name = models.CharField(max_length=25)
    filename = models.CharField(max_length=25)
    created_on = models.DateField(default=dt.today)

    def __str__(self):
        return str(self.name)
