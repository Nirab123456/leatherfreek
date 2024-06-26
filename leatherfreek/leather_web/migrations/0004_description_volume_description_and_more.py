# Generated by Django 5.0.6 on 2024-06-25 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leather_web', '0003_alter_home_product_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('description_id', models.AutoField(primary_key=True, serialize=False)),
                ('text_description', models.TextField()),
                ('weight_description', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Volume_Description',
            fields=[
                ('volume_description_id', models.AutoField(primary_key=True, serialize=False)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('depth', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vollume', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='display_product',
            name='product_description',
            field=models.ManyToManyField(to='leather_web.description'),
        ),
        migrations.AddField(
            model_name='description',
            name='volume_description',
            field=models.ManyToManyField(to='leather_web.volume_description'),
        ),
    ]
