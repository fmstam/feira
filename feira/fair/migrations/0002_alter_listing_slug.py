# Generated by Django 3.2.8 on 2021-10-18 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='slug',
            field=models.SlugField(default='title', max_length=128, unique_for_date='creation_date'),
        ),
    ]
