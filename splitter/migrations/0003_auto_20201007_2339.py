# Generated by Django 3.1.2 on 2020-10-08 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splitter', '0002_auto_20201007_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='tip',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]
