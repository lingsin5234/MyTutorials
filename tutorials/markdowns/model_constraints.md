## Unique Constraints
To add unique constrains, under the corresponding model, add a `Constraint` under `class Meta`:
```python
class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),
        ]
```

## References
[Model Options](https://docs.djangoproject.com/en/3.0/ref/models/options/#django.db.models.Options.constraints)  
[Unique Constraint](https://docs.djangoproject.com/en/3.0/ref/models/constraints/#django.db.models.UniqueConstraint)  