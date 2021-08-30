# Generated by Django 3.1.5 on 2021-08-29 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0015_auto_20210829_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='category',
        ),
        migrations.AddField(
            model_name='policy',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.category'),
        ),
    ]