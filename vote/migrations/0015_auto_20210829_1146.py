# Generated by Django 3.1.5 on 2021-08-29 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0014_auto_20210829_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='category',
            field=models.ManyToManyField(blank=True, to='vote.Category'),
        ),
    ]