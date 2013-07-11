from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pongtracker.views.home', name='home'),
    # url(r'^pongtracker/', include('pongtracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^games/create/$','Game.views.createNewGameRequest'),
     url(r'^games/(?P<game_id>\d+)/$','Game.views.getGame'),
     url(r'^$',TemplateView.as_view(template_name = "index.html"))