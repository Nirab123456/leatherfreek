# Generated by Django 5.0.6 on 2024-07-08 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leather_web', '0022_alter_volume_description_vollume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_record',
            name='user_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user_record',
            name='user_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
