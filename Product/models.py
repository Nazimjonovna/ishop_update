from django.db import models
from Admin.models import Admin

class Product(models.Model):
    quantity = models.IntegerField(null=True)
    cost = models.FloatField(null=True)
    time = models.DateTimeField(auto_now=True)
    prosent = models.FloatField(null=True, blank=True)
    postavshik = models.CharField(max_length=2000, null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    tasdiq = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cost)

class Category(models.Model):
    name = models.CharField(max_length=100, choices=(
        ('Maishiy_texnika', 'Maishiy_texnika'),
        ('Noutbooklar', 'Noutbooklar'),
        ('Smartfonlar', 'Smartfonlar'),
        ('Planshetlar', 'Planshetlar'),
        ("Aksesuarlar", 'Aksesuarlar'),
        ("Maishiy_texnika", 'Maishiy_texnika'),
        ('Texnika', 'Texnika'),
        ('Atir', 'Atir'),
        ('kitob', 'kitob'),
        ('Avtobar', 'Avtobar'),
    ))

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category_choices = [
        ('Maishiy_texnika', [
            ('SubCat1', 'SubCat1'),
            ('SubCat2', 'SubCat2'),
        ]),
        ('Noutbooklar', [
            ('SubCat3', 'SubCat3'),
            ('SubCat4', 'SubCat4'),
        ]),
        ('Smartfonlar', [
            ('SubCat5', 'SubCat5'),
            ('SubCat6', 'SubCat6'),
        ]),
    ]

    category = models.CharField(max_length=100, choices=category_choices)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductInfo(models.Model):
    lang = (
        ('Rus', 'Rus'),
        ('Uzbek', 'Uzbek'),
    )

    language = models.CharField(max_length=20, choices=lang)
    name = models.CharField(max_length=250, null=True)
    about = models.TextField(null=True)
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    model = models.CharField(max_length=250, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Image(models.Model):
    color_key = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class RecPro(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rec_pro')
    is_rec = models.BooleanField(default=True)

    def __str__(self):
        return str(self.is_rec)
