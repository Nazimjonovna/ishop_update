# Generated by Django 5.0.1 on 2024-02-06 09:27

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message='Telefon raqamini +998XXXXXXXXX kabi kiriting!', regex='d{0,9}')])),
                ('otp', models.CharField(max_length=4, null=True)),
                ('card', models.IntegerField()),
                ('card_info', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='ValidatedOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message='Telefon raqamini +9989XXXXXXXX kabi kiriting!', regex='d{0,9}')])),
                ('otp', models.CharField(blank=True, max_length=9, null=True)),
                ('count', models.IntegerField(default=0, help_text='Kodni kiritishlar soni:')),
                ('validated', models.BooleanField(default=False, help_text='Shaxsiy kabinetingizni yaratishingiz mumkin!')),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=9, unique=True)),
                ('verify_code', models.SmallIntegerField()),
                ('is_verified', models.BooleanField(default=False)),
                ('step_reset', models.CharField(blank=True, choices=[('send', 'send'), ('confirmed', 'confirmed')], max_length=10, null=True)),
                ('step_change_phone', models.CharField(blank=True, choices=[('send', 'send'), ('confirmed', 'confirmed')], max_length=30, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paspord_raqam', models.CharField(max_length=6, null=True)),
                ('paspord_seria', models.CharField(max_length=3, null=True)),
                ('paspord', models.ImageField(null=True, upload_to='pasportlar/')),
                ('image', models.ImageField(null=True, upload_to='rasmlar/')),
                ('adress', models.TextField(null=True)),
                ('viloyat', models.CharField(choices=[('Toshkent', 'Toshkent'), ('Navoiy', 'Navoiy'), ('Buxoro', 'Buxoro'), ('Samarqand', 'Samarqand'), ('Jizzax', 'Jizzax'), ('Xorazm', 'Xorazm'), ('Sirdaryo', 'Sirdaryo'), ('Namangan', 'Namangan'), ("Farg'ona", "Farg'ona"), ('Andijon', 'Andijon'), ('Qashqadaryo', 'Qashqadaryo'), ('Surxandaryo', 'Surxandaryo'), ('Nukus', 'Nukus')], max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
        ),
    ]
