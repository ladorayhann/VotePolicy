# Generated by Django 3.1.5 on 2021-03-26 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='statusVote',
        ),
        migrations.AddField(
            model_name='statusvote',
            name='vote',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.vote'),
        ),
    ]
