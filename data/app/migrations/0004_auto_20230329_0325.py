# Generated by Django 3.2.18 on 2023-03-29 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20230329_0319'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pollingunit',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='ward',
            options={'managed': False},
        ),
    ]