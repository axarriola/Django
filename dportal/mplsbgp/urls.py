from django.conf.urls import url

from . import views
app_name = 'mplsbgp'
urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^mpls/$', views.mpls, name='mpls'),
        url(r'^mplsresult/$', views.mplsresult, name='mplsresult'),
        url(r'^bgp/$', views.bgp, name='bgp'),
        url(r'^bgpresult/$', views.bgpresult, name='bgpresult'),
    ]
