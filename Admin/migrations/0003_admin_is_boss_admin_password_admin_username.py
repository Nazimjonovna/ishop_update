# Generated by Django 5.0.1 on 2024-02-13 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_protsent'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='is_boss',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='admin',
            name='password',
            field=models.CharField(default=1, max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admin',
            name='username',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
