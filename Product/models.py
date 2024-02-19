from django.db import models
from Admin.models import Admin, Protsent


class Costs(models.Model):
    costs = models.IntegerField()
    def __str__(self):
        return str(self.costs)


class Product(models.Model):
    quantity = models.IntegerField(null=True)
    cost = models.FloatField(null=True)
    time = models.DateTimeField(auto_now=True)
    protsent = models.ManyToManyField(Protsent)
    postavshik = models.CharField(max_length=2000, null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    tasdiq = models.BooleanField(default=False)
    cre_cost = models.ManyToManyField(Costs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.cre_cost.exists():
            default_cost = Costs.objects.create(costs=0)
            self.cre_cost.add(default_cost)

        new_cre_cost_instances = []

        for protsent_instance in self.protsent.all():
            calculated_cost = self.cost * (1 + (protsent_instance.protsent / 100)) / 12
            cost_instance = Costs.objects.create(costs=calculated_cost)
            new_cre_cost_instances.append(cost_instance)
        self.cre_cost.clear()
        self.cre_cost.add(*new_cre_cost_instances)


class Category(models.Model):
    name = models.CharField(max_length=100, choices=(
        ('Maishiy_texnika', 'Maishiy_texnika'),
        ('Noutbooklar', 'Noutbooklar'),
        ('Smartfonlar', 'Smartfonlar'),
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
        ('Smartfonlar', (
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
            ('boshqa', 'boshqa'),
        )),
        ("Noutbooklar", (
            ('Macbook', 'Macbook'),
            ('HP', 'HP'),
            ('Lenova', 'Lenova'),
            ('Acer', 'Acer'),
            ('Samsung', 'Samsung'),
            ('Dell', 'Dell'),
            ('MSI', 'MSI'),
            ('Asus', 'Asus'),
            ('boshqa', 'boshqa'),
        )),
        ('Aksesuarlar', (
            ('Microfon', 'Microfon'),
            ('Klaviatura', 'Klaviatura'),
            ('Sumka', 'Sumka'),
            ('Sichqoncha', 'Sichqoncha'),
            ('Printer', 'Printer'),
            ('Quloqchin', 'Quloqchin'),
            ('boshqa', 'boshqa'),
        )),
        ('Maishiy_texnika', (
            ('Changyutgich', 'Changyutgich'),
            ('Kuller', 'Kuller'),
            ('Dazmol', 'Dazmol'),
            ('Televizor', 'Televizor'),
            ('Muzlatgich', 'Muzlatgich'),
            ('Kir yuvish mashinasi', 'Kir yuvish mashinasi'),
            ('konditsioner', 'konditsioner'),
            ('Gaz plita', 'Gaz plita'),
            ('boshqa', 'boshqa'),
        )),
        ('Atir', (
            ('Ayol', 'Ayol'),
            ('Erkak', 'Erkak'),
        )),
        ('kitob', (
            ('Diniy', 'Diniy'),
            ('Badiiy', 'Badiiy'),
        )),
        ('Autobar', (
            ("Autobar", 'Autobar'),
        ))
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
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='rec_pro')
    is_rec = models.BooleanField(default=True)
    about = models.TextField()

    def __str__(self):
        return str(self.is_rec)
