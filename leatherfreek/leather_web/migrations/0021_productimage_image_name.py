# Generated by Django 5.0.6 on 2024-07-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leather_web', '0020_checkout_checkoutitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='image_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
