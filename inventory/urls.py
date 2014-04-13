from django.conf.urls import patterns, url

from inventory import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /inventory/5/
    url(r'^(?P<inventory_id>\d+)/$', views.detail, name='detail'),
)
