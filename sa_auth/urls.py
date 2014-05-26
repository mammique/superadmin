# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import reception, logout_view

urlpatterns = patterns('',
    url(r'^$', reception, name='reception'),
    url(r'^auth/logout/$', logout_view, name='logout'),
)
