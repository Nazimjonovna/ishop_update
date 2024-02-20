from django.db import models
from Product.models import *

# Create your models here.
class Reclama(models.Model):
    image = models.FileField(upload_to='reclama/')
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Categoryreclama(models.Model):
    choise = (
        ('Apple', 'Apple'),
        ('Samsung', 'Samsung'),
        ('Honor', 'Honor'),
        ('Xiaomi', 'Xiaomi'),
        ('Vivo', 'Vivo'),
        ('Realme', 'Realme'),
        ('Huawei', 'Huawei'),
        ('OPPO', 'OPPO'),
        ('Tecno', 'Tecno'),
        ('Planshetlar', 'Planshetlar'),
        ('Macbook', 'Macbook'),
        ('HP', 'HP'),
        ('Lenova', 'Lenova'),
        ('Acer', 'Acer'),
        ('Samsung', 'Samsung'),
        ('Dell', 'Dell'),
        ('MSI', 'MSI'),
        ('Asus', 'Asus'),
        ('Microfon', 'Microfon'),
        ('Klaviatura', 'Klaviatura'),
        ('Sumka', 'Sumka'),
        ('Sichqoncha', 'Sichqoncha'),
        ('Printer', 'Printer'),
        ('Quloqchin', 'Quloqchin'),
        ('Changyutgich', 'Changyutgich'),
        ('Kuller', 'Kuller'),
        ('Dazmol', 'Dazmol'),
        ('Televizor', 'Televizor'),
        ('Muzlatgich', 'Muzlatgich'),
        ('Kir yuvish mashinasi', 'Kir yuvish mashinasi'),
        ('konditsioner', 'konditsioner'),
        ('Gaz plita', 'Gaz plita'),
        ('Atir', 'Atir'),
        ('Kitoblar', 'Kitoblar'),
        ("Autobar", 'Autobar'))
    category = models.CharField(max_length=20, choices=choise)
    image = models.FileField(upload_to='category_rec/')
    name = models.CharField(max_length=20, null = True)

    def __str__(self):
        return self.category


class RecCard(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='card_rec/')
    name = models.CharField(max_length=200)
    about = models.TextField()

    def __str__(self):
        return self.name

