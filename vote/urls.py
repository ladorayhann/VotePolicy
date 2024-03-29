from django.contrib import admin
from django.urls import path
from vote import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    # progress
    path('create_seruan', views.campaign_make, name='campaign_make'),
    path('seruan', views.campaign_home, name='campaign_home'),
    path('seruan_search', views.campaign_search, name='campaign_search'),
    path('vote/detail/<int:id>', views.vote_detail, name='vote_detail'),
    path('kebijakan', views.kebijakan_search, name='kebijakan_search'),
    path('kebijakan/detail/<int:id>', views.kebijakan_detail, name='kebijakan_detail'),
    path('kebijakan/add', views.kebijakan_add, name='kebijakan_add'),
    path('profile', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
]