# Generated by Django 3.2.5 on 2021-11-01 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0026_alter_listing_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='slug',
            field=models.SlugField(max_length=128),
        ),
    ]
