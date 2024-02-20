from django.db import models

# Create your models here.
class partner(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    pass
