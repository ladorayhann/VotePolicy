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
    path('campaign_home', views.campaign_home, name='campaign_home'),
    path('campaign_detail', views.campaign_detail, name='campaign_detail'),
    path('campaign_search', views.campaign_search, name='campaign_search'),
    path('vote', views.vote, name='vote'),
    path('vote/detail', views.vote_detail, name='vote_detail'),
    path('kebijakan', views.kebijakan_search, name='kebijakan_search'),
    path('kebijakan/detail/<int:id>', views.kebijakan_detail, name='kebijakan_detail'),
    path('kebijakan/add', views.kebijakan_add, name='kebijakan_add'),
    path('profile', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
]