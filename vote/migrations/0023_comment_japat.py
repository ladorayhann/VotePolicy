# Generated by Django 3.1.5 on 2021-08-29 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0022_remove_comment_japat'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='japat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.japat'),
        ),
    ]
