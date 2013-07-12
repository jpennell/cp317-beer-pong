from django.conf.urls import patterns, url

from User import views

urlpatterns = patterns('',
    (r'index/$', 'User.views.loginUser'),
    (r'index/logout', 'User.views.logoutUser'),
    (r'profile/$', 'User.views.viewProfile'),
)