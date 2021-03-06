# Generated by Django 3.2.8 on 2021-10-25 10:11

from django.db import migrations, models
import fair.encryptions


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0017_alter_deleteddata_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='action',
            field=fair.encryptions.EncryptedTextField(),
        ),
        migrations.AlterField(
            model_name='deleteddata',
            name='data',
            field=models.TextField(),
        ),
    ]
