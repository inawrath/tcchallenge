# Generated by Django 3.1.6 on 2021-02-07 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210207_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
