from django.conf.urls import patterns, url

from User import views

urlpatterns = patterns('',
    (r'index/$', 'User.views.loginUserRequest'),
    
    (r'login', 'User.views.loginUserRequest'),
    (r'logout', 'User.views.logoutUser'),
    (r'profile/(?P<user_username>\d+)/$', 'User.views.viewProfile'),
    (r'profile/edit','User.views.editProfileView'),
    (r'register','User.views.registerNewUser'),
)