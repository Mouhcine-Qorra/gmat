# Generated by Django 3.2.5 on 2021-09-19 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_customer_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='ip',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
