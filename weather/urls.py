

from django.conf.urls import patterns, url
from weather import views

urlpatterns = patterns('',
    url(r'^info/(?P<loccode>\d{9})$', views.getweatherinfo, name='getweatherinfo'),
    #url(ur'^info/(?P<locstr>([^/]+))$', views.getweatherinfoconv, name='getweatherinfo'),
    url(r'^info/(?P<locstr>([^/]+))$', views.getweatherinfoconv, name='getweatherinfo'),
    url(r'^info/(?P<lat>([0-9.-]+))/(?P<lon>([0-9.-])+)$', views.getweatherfromloc, name="getweatherfromloc"),
)
