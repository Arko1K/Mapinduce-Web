from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Mapsnap.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^nextpolygon', 'polyedit.views.get_next_polygon', name='nextpolygon'),
    url(r'^nextchrome', 'polyedit.views.get_next_place_chrome', name='nextchrome'),
    url(r'^next', 'polyedit.views.get_next_place', name='next'),
    url(r'^put', 'polyedit.views.save_vertex', name='put'),
    url(r'^reset', 'polyedit.views.reset', name='reset'),
    url(r'^image', 'polyedit.views.upload_image', name='image'),
    url(r'^', 'polyedit.views.home', name='home')
)