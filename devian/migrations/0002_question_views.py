# Generated by Django 3.2.15 on 2022-09-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devian', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
