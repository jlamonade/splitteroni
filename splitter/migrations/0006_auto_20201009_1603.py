# Generated by Django 3.1.2 on 2020-10-09 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splitter', '0005_merge_20201009_1438'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='bill',
            index=models.Index(fields=['id'], name='id_index'),
        ),
    ]