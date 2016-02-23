"""Wnioskodator URL Configuration

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
#from django.contrib import admin

from User import views as user_views
from Application import views as application_view
from Home import views as home_views

urlpatterns = [
    ### AUTH - TOKEN ###
    url(r'^api/auth/$', application_view.getAuthToken),

    ### API URLS ###
    url(r'^api/applications_list/$', application_view.applications_list),
    url(r'^api/application_detail/(?P<pk>[0-9]+)/$', application_view.application_detail),

    ### USER URLS ###
    url(r'^$', user_views.login),
    url(r'^login/$', user_views.login),
    url(r'^logout/$', user_views.logout),
    url(r'^changepassword/$', user_views.changepassword),

    ### HOME URLS ###
    url(r'^home/$', home_views.home)




]
