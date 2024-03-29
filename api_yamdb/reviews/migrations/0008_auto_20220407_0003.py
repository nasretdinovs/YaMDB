# Generated by Django 2.2.16 on 2022-04-06 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220406_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yamdbuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='yamdbuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='yamdbuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='ник'),
        ),
    ]
