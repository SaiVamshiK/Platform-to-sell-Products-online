# Generated by Django 3.1 on 2020-08-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20200830_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]