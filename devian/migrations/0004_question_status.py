# Generated by Django 3.2.15 on 2022-10-02 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devian', '0003_auto_20220922_0413'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=100),
        ),
    ]