# Generated by Django 5.0.1 on 2024-03-10 02:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0006_remove_product_cre_cost_product_partner_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoryreclama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Apple', 'Apple'), ('Samsung', 'Samsung'), ('Honor', 'Honor'), ('Xiaomi', 'Xiaomi'), ('Vivo', 'Vivo'), ('Realme', 'Realme'), ('Huawei', 'Huawei'), ('OPPO', 'OPPO'), ('Tecno', 'Tecno'), ('Planshetlar', 'Planshetlar'), ('Macbook', 'Macbook'), ('HP', 'HP'), ('Lenova', 'Lenova'), ('Acer', 'Acer'), ('Samsung', 'Samsung'), ('Dell', 'Dell'), ('MSI', 'MSI'), ('Asus', 'Asus'), ('Microfon', 'Microfon'), ('Klaviatura', 'Klaviatura'), ('Sumka', 'Sumka'), ('Sichqoncha', 'Sichqoncha'), ('Printer', 'Printer'), ('Quloqchin', 'Quloqchin'), ('Changyutgich', 'Changyutgich'), ('Kuller', 'Kuller'), ('Dazmol', 'Dazmol'), ('Televizor', 'Televizor'), ('Muzlatgich', 'Muzlatgich'), ('Kir yuvish mashinasi', 'Kir yuvish mashinasi'), ('konditsioner', 'konditsioner'), ('Gaz plita', 'Gaz plita'), ('Atir', 'Atir'), ('Kitoblar', 'Kitoblar'), ('Autobar', 'Autobar')], max_length=20)),
                ('image', models.FileField(upload_to='category_rec/')),
                ('name', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reclama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='reclama/')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='card_rec/')),
                ('name', models.CharField(max_length=200)),
                ('about', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product')),
            ],
        ),
    ]
