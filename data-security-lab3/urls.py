"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import views, api

import api

urlpatterns = [
    url(r'^/$', views.index),
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # fs
    url(r'^login/', api.login),
    url(r'^x/', api.get_x),
    url(r'^logged/', api.logged),
    url(r'^logout/', api.logout),
    url(r'^check-captcha/', api.check_captcha),
    url(r'^read/(?P<path>\w{0,100})', api.read),
    url(r'^write/(?P<path>\w{0,1000})', api.write),
    url(r'^execute/(?P<path>\w{0,100})', api.execute),
    url(r'^delete/(?P<path>\w{0,100})', api.delete)
]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
