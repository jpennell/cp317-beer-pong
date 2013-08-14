from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


from django.conf import settings

from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( '',
# Examples:
# url(r'^$', 'pongtracker.views.home', name='home'),
# url(r'^pongtracker/', include('pongtracker.foo.urls')),

# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment the next line to enable the admin:

	url( r'^admin/', include( admin.site.urls ) ),
	url( r'^game/', include( 'Game.urls' ) ),
	url( r'^', include( 'User.urls' ) ),
	url( r'^rules', TemplateView.as_view( template_name = "pongtracker/rules.html" ), name = "rules" ),
	url( r'^', include( 'Statistics.urls' ) ),
	url( r'^$', 'User.views.viewHomepageRequest', name = "index" ),
 )

if settings.DEBUG:
	urlpatterns += patterns( 'django.contrib.staticfiles.views',
		url( r'^static/(?P<path>.*)$', 'serve' ),
 	)

	urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
