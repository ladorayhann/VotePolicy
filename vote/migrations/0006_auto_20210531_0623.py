# Generated by Django 3.1.5 on 2021-05-31 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_auto_20210326_0913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='japat',
            old_name='Category',
            new_name='category',
        ),
    ]
