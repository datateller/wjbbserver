'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from dianping import views

urlpatterns = patterns('',
    url(r'^getbusinessbasic/', views.getbusinessbasic, name='getbusinessbasic'),
    url(r'^getbusinessbyid/', views.getbusinessbyid, name='getbusinessbyid'),
)