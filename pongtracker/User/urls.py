from django.conf.urls import patterns, url

from User import views

urlpatterns = patterns('',
    (r'index/$', 'User.views.loginUserRequest'),
    
    (r'login', 'User.views.loginUserRequest'),
    (r'logout', 'User.views.logoutUser'),
    (r'profile/(?P<user_id>\d+)/$', 'User.views.viewProfile'),
    (r'editProfile','User.views.registerNewUser'),
    (r'register','User.views.registerNewUser'),
)