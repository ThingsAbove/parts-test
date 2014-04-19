from django.conf.urls import patterns, url

from inventory import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^parts/$', views.all_parts, name='all_parts'),
    url(r'^parts/(?P<part_class>[A-C]{1})/$', views.parts_by_class, name='parts_by_class'),
    # ex: /inventory/5/
    url(r'^(?P<inventory_id>\d+)/$', views.detail, name='detail'),
)
