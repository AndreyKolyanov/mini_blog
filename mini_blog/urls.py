"""lab4 URL Configuration

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
from userlist.views import user_list
from account.views import user_profile, add, user_settings, change_settings, remove, update, subscribe
from login.views import log, logging, logout_user, new_user, registration
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/$', user_list),
    url(r'^$', user_list),
    url(r'^log/$', log),
    url(r'^login/error/(?P<error>[1-9]+)/$', logging),
    url(r'^login/$', logging),
    url(r'^logout/$', logout_user),
    url(r'^registration/error/(?P<error>[1-9]+)$', new_user),
    url(r'^registration/$', new_user),
    url(r'^newusr/$', registration),
    url(r'^id(?P<user_id>\d+)/(?P<page>\d+)/$', user_profile),
    url(r'^id(?P<user_id>\d+)/$', user_profile),
    url(r'^settings/$', user_settings),
    url(r'^change_settings/$', change_settings),
    url(r'^add/$', add),
    url(r'^remove/$', remove),
    url(r'^update/$', update),
    url(r'^subscribe/$', subscribe)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
