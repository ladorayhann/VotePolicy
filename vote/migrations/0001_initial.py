# Generated by Django 3.1.5 on 2021-03-26 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deskripsi', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Japat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('target', models.CharField(default='', max_length=100)),
                ('content', models.TextField(default='')),
                ('image', models.ImageField(upload_to='')),
                ('file1', models.FileField(upload_to='')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('Category', models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.category')),
            ],
        ),
        migrations.CreateModel(
            name='StatusJapat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deskripsi', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StatusVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statusVote', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('japat', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='vote.japat')),
                ('statusVote', models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.statusvote')),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('content', models.TextField()),
                ('spotify', models.URLField(null=True)),
                ('youtube', models.URLField(null=True)),
                ('instagram', models.URLField(null=True)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.category')),
            ],
        ),
        migrations.AddField(
            model_name='japat',
            name='statusJapat',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.statusjapat'),
        ),
        migrations.AddField(
            model_name='japat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_policy', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('policy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.policy')),
                ('vote', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='vote.vote')),
            ],
        ),
    ]
