from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'partstest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('inventory.urls')),
    url(r'^about/', 'partstest.views.about', name='about'),
    url(r'^contact/', 'partstest.views.contact', name='contact'),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/',  include(admin.site.urls)), # admin site
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'},
        name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='mysite_logout'),
)