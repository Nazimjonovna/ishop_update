from django.db import models

# Create your models here.
class Admin(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=8)
    is_boss = models.BooleanField(default=False)


    def __str__(self):
        return self.username

class Protsent(models.Model):
    protsent = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


