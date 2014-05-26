# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'superadmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('sa_auth.urls', namespace='sa_auth', app_name='sa_auth')),
    url(r'^admin/', include(admin.site.urls)),
)
