# Generated by Django 3.2.5 on 2021-09-27 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_shippingadress_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingadress',
            name='address',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='shippingadress',
            name='phone',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='shippingadress',
            name='state',
            field=models.CharField(max_length=100, null=True),
        ),
    ]