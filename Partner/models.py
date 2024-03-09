from django.db import models

# Create your models here.
class Partner(models.Model):
    name = models.CharField(max_length = 500)
    phone = models.CharField(max_length = 200)
    adress = models.TextField()
    

    def __str__(self) -> str:
        return self.name
    
    


