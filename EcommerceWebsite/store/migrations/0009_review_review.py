# Generated by Django 3.1 on 2020-08-31 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20200830_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]