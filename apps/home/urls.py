# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*html', views.pages, name='pages'),
    
    # The home page
    path('user/<id>', views.student_page, name='user'),
    path('user/<id>/todo/', views.to_do_list, name='todo'),


]
