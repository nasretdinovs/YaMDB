# Generated by Django 2.2.16 on 2022-04-04 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.TextField(verbose_name='название категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.TextField(verbose_name='название жанра'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.TextField(verbose_name='название'),
        ),
    ]
