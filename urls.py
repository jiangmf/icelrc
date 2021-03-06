"""icelrc URL Configuration

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
from django.apps import apps

from icelrc import views

class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [model.__str__] + [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


for model in apps.get_app_config('icelrc').get_models():
   admin.site.register(model, CustomModelAdmin)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', views.lyrics_admin),
]
