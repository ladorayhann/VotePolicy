from django.db import models
from datetime import datetime, timedelta, tzinfo
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    deskripsi = models.CharField(max_length=50)

    def __str__(self):
        return f'Category : {self.deskripsi}'

class StatusJapat(models.Model):
    deskripsi = models.CharField(max_length=20)

    def __str__(self):
        return f'StatusJapat : {self.deskripsi}'

class Japat(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    voters = models.IntegerField(null=True, blank=True, default=0)
    statusJapat = models.ForeignKey(StatusJapat, null=True, on_delete=models.RESTRICT, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.RESTRICT, blank=True)
    title = models.CharField(max_length=100, unique=False)
    target = models.CharField(max_length=100, null=False, default="")
    content = models.TextField(null=False, default="")
    image = models.ImageField(null=True, blank=True)
    file1 = models.FileField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Japat : {self.title}'

class StatusVote(models.Model):
    statusVote = models.BooleanField()
    

    def __str__(self):
        if self.statusVote:
            return f'Status Vote : Setuju'
        else:
            return f'Status Vote : Tidak Setuju'
        

class Vote(models.Model):
    japat = models.ForeignKey(Japat, on_delete=models.RESTRICT)
    email = models.EmailField()
    statusVote = models.OneToOneField(StatusVote, null=True, on_delete=models.RESTRICT)
    
    def __str__(self):
        return f'Vote : {str(self.japat.title)}'

class Policy(models.Model):
    title = models.CharField(max_length=1000, unique=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.RESTRICT, blank=True)
    content = models.TextField(null=False)
    overview = models.TextField(null=True)
    spotify = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Policy Title : {self.title}'

class Comment(models.Model):
    content = models.CharField(max_length=100)
    policy = models.ForeignKey(Policy, null=True, on_delete=models.RESTRICT, blank=True)
    vote = models.ForeignKey(Vote, null=True, on_delete=models.RESTRICT, blank=True)
    created_time = models.DateTimeField(default=timezone.now)
    is_policy = models.BooleanField()
    email = models.EmailField()

    def __str__(self):
        if self.is_policy:
            comment = 'Policy'
            return f'Comment {comment} {self.policy.title}'
        else:
            comment = 'Vote'
            return f'Comment {comment} {self.vote.japat.title}'
        






