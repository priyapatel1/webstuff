#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:49:20 2021

@author: priyapatel
"""

from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
]

