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


from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from cinema.views import ScreeningsListView, ScreeningsDetailView,login,logout,screening,register


admin.autodiscover()  #функция автоматического обнаружения файлов admin.py в наших приложениях

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)), #URL админки http://имя_сайта/admin/
    url(r'^cinema/$', ScreeningsListView.as_view(), name='list'), # то есть по URL http://имя_сайта/blog/
                                               # будет выводиться список постов
    url(r'^cinema/(?P<rid>\d+)/$', 'cinema.views.screening'),
    url(r'^cinema/login/$',  login),
    url(r'^cinema/logout/$', logout),
    url(r'^cinema/register/$', 'cinema.views.register')
)
