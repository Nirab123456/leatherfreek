# Generated by Django 5.0.6 on 2024-06-24 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leather_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leather_web.display_product')),
            ],
        ),
    ]
