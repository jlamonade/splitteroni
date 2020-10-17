# Generated by Django 3.1.2 on 2020-10-15 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('splitter', '0010_bill_tax_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='tip_percent',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
    ]