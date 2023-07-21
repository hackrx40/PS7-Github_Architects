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
    path('login/dashboard/', views.dashboard, name='dashboard'),
    path('generateDataFromTwitter/', views.generateDataForTwitter, name='generateDataFromTwitter'),
    path('generateDataFromInsta/', views.generateDataForInsta, name='generateDataFromInsta'),
    path('generateLeads/', views.generateLeads, name='generateLeads'),
    path('dataVisualization/', views.dataVisualization, name='dataVisualization'),
    path('sales-analysis',views.sales_analytics,name='sales-analytics'),
    path('approve_employee/', views.approve_employee_view, name='approve_employee'),
    path('todo/', views.todo, name='todo'),
    path('settings/', views.settings, name='settings'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('analysis/',views.analysis,name='analysis'),
    path('competitors/', views.competitorAnalysis, name="competitors"),
]
