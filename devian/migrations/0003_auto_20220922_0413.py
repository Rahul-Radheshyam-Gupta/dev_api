# Generated by Django 3.2.15 on 2022-09-22 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devian', '0002_question_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='down_vote_list',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='answer',
            name='up_vote_list',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='question',
            name='down_vote_list',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='question',
            name='up_vote_list',
            field=models.TextField(default='[]'),
        ),
    ]