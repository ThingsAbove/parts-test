try:
    from django.conf.urls import *
except:
    from django.conf.urls.defaults import *
from django.conf.urls.static import static
from inventory import views
from ajax_select import urls as ajax_select_urls

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^part/edit/(?P<id>\d+)?$', views.edit_part, name='edit_part'),
    url(r'^parts/$', views.parts_list, name='parts_list'),
    
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

    url(r'^piechart/$', views.piechart, name='piechart'),
    url(r'^barchart/$', views.barchart, name='barchart'),
    url(r'^(?P<inventory_id>\d+)/linechart/$', views.linechart, name='linechart'),

    # ex: /inventory/5/
    url(r'^(?P<inventory_id>\d+)/$', views.detail, name='detail'),
)
