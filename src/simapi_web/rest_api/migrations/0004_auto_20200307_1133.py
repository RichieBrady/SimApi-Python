# Generated by Django 3.0.3 on 2020-03-07 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_filemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='file',
            field=models.FileField(default='', upload_to='./Media/'),
        ),
    ]