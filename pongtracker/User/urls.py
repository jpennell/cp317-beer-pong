from django.conf.urls import patterns, url

from User import views

urlpatterns = patterns('',
    (r'index/$', 'User.views.loginUserRequest'),
    (r'index/logout', 'User.views.logoutUser'),
    (r'profile/$', 'User.views.viewProfile'),
    (r'register','User.views.registerNewUser'),
    (r'editProfile','User.views.registerNewUser'),
)