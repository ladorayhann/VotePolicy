from django.contrib import admin
from django.urls import path
from vote import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    # progress
    path('campaign_make', views.campaign_make, name='campaign_make'),
]