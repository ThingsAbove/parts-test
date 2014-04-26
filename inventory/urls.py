from django.conf.urls import patterns, url

from inventory import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^parts/$', views.parts_list, name='parts_list'),
    url(r'^parts/(?P<part_class>[A-C]{1})/$', views.parts_by_class, name='parts_by_class'),
    url(r'^piechart/$', views.piechart, name='piechart'),
    url(r'^barchart/$', views.barchart, name='barchart'),
    url(r'^(?P<inventory_id>\d+)/linechart/$', views.linechart, name='linechart'),

    # ex: /inventory/5/
    url(r'^(?P<inventory_id>\d+)/$', views.detail, name='detail'),
)
