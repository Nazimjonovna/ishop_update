from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_regex = RegexValidator(regex='d{0,9}', message="Telefon raqamini +998XXXXXXXXX kabi kiriting!")
    phone = models.CharField(validators=[phone_regex], max_length=9, unique=True)
    otp = models.CharField(max_length=4, null=True)
    card = models.IntegerField()
    card_info = models.CharField(max_length=4)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.name

class Userdata(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paspord_raqam = models.CharField(max_length=6, null=True)
    paspord_seria = models.CharField(max_length=3, null=True)
    paspord = models.ImageField(upload_to='pasportlar/', null=True)
    image = models.ImageField(upload_to='rasmlar/', null=True)
    adress = models.TextField(null=True)
    vil = (
        ('Toshkent', 'Toshkent'),
        ('Navoiy', 'Navoiy'),
        ('Buxoro', 'Buxoro'),
        ('Samarqand', 'Samarqand'),
        ('Jizzax', 'Jizzax'),
        ('Xorazm', 'Xorazm'),
        ('Sirdaryo', 'Sirdaryo'),
        ('Namangan', 'Namangan'),
        ("Farg'ona", "Farg'ona"),
        ('Andijon', 'Andijon'),
        ('Qashqadaryo', 'Qashqadaryo'),
        ('Surxandaryo', 'Surxandaryo'),
        ('Nukus', 'Nukus')
    )
    viloyat = models.CharField(max_length=200, choices=vil, null=True)

    def __str__(self):
        return self.adress

class ValidatedOtp(models.Model):
    phone_regex = RegexValidator(regex='d{0,9}', message="Telefon raqamini +9989XXXXXXXX kabi kiriting!")
    phone = models.CharField(validators=[phone_regex],max_length=9,unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Kodni kiritishlar soni:')
    validated = models.BooleanField(default=False, help_text="Shaxsiy kabinetingizni yaratishingiz mumkin!")

    def __str__(self):
        return str(self.phone)

class Verification(models.Model):
    STATUS = (
        ('send', 'send'),
        ('confirmed', 'confirmed'),
    )
    phone = models.CharField(max_length=9, unique=True)
    verify_code = models.SmallIntegerField()
    is_verified = models.BooleanField(default=False)
    step_reset = models.CharField(max_length=10, null=True, blank=True, choices=STATUS)
    step_change_phone = models.CharField(max_length=30, null=True, blank=True, choices=STATUS)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} --- {self.verify_code}"



