from django.db import models
from Admin.models import Admin, Protsent
from Partner.models import *
from django.core.validators import RegexValidator
from User.models import User


class Product(models.Model):
    partner = models.ForeignKey(Partner, on_delete = models.CASCADE, null = True, blank = True)
    quantity = models.IntegerField(null=True)
    cost = models.FloatField(null=True)
    time = models.DateTimeField(auto_now=True)
    protsent = models.ManyToManyField(Protsent)
    postavshik = models.CharField(max_length=2000, null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    tasdiq = models.BooleanField(default=False)
    cre_cost = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
            if self.pk is None:
                admin_instances = Protsent.objects.all()
                cre_cost_dict = {}
                for admin_instance in admin_instances:
                    cre_cost_dict[admin_instance.pk] = admin_instance.protsent * self.cost
                self.cre_cost = cre_cost_dict
            super().save(*args, **kwargs)


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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    name_credit = models.ForeignKey(Protsent, on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    stat = (
        ('buyurtma_berish', 'buyurtma_berish'),
        ('buyurtma_tayyorlanmoqda', 'buyurtma_tayyorlanmoqda'),
        ('yetkazib_berish_jarayoni', 'yetkazib_berish_jarayoni'),
        ('yetkazilgan', 'yetkazilgan'),
        ('bekor_qilingan', 'bekor_qilingan')
    )
    state = models.CharField(max_length=200, choices=stat, default='buyurtma_berish')
    pay = (
        ('naqt', 'naqt'),
        ('card', 'card'),
        ('credit', 'credit')
    )
    payment = models.CharField(max_length=100, choices=pay, default='naqt')
    quantity = models.IntegerField(null=True)
    rat = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    rate = models.CharField(max_length=10, choices=rat, default=1, null=True)
    pro = (
        ('is_buy', 'is_buy'),
        ('is_like', 'is_like')
    )
    pro_x = models.CharField(max_length=50, choices=pro, null=True)
    oy = models.IntegerField()
    phone_regex = RegexValidator(regex='d{0,9}', message="Telefon raqamini +998XXXXXXXXX kabi kiriting!")
    phone_cre = models.CharField(validators=[phone_regex], max_length=9, unique=True, null=True)
    tasdiq = models.BooleanField(null=True)
    color = models.CharField(max_length=120, null=True)
    cost_order = models.FloatField(blank=True, null=True)

    def str(self):
        return str(self.time)