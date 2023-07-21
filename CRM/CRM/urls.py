"""
URL configuration for CRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from CRM import views
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path('', lambda request: redirect('login/', permanent=False)),
    path('instagram/profile/', views.get_instagram_profile, name='instagram-profile'),
    path('instagram/stats/', views.get_instagram_stats, name='instagram-stats'),
    path('instagram-posts/', views.get_instagram_posts, name='get_instagram_posts'),
    path('subreddit-data/', views.get_subreddit_data, name='get_subreddit_data'),
    path('tweets/', views.get_tweets, name='get_tweets'),
]
