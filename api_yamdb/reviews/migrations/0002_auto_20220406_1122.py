# Generated by Django 2.2.16 on 2022-04-06 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yamdbuser',
            name='is_moderator',
        ),
        migrations.AddField(
            model_name='yamdbuser',
            name='role',
            field=models.CharField(choices=[('user', 'пользователь'), ('admin', 'админ'), ('moderator', 'модератор')], default='user', max_length=10),
        ),
    ]