from django.conf.urls import url

from . import views
app_name = 'cfgdev'
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^cfginput/$', views.cfginput, name='cfginput'),
        url(r'^cfgpreview/$', views.cfgpreview, name='cfgpreview'),
        url(r'^commit/$', views.commit, name='commit'),
        url(r'^rollback/$', views.rollback, name='rollback'),
    ]
