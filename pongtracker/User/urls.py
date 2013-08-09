from django.conf.urls import patterns, url

from User import views

urlpatterns = patterns( '',
    url( r'index/$', 'User.views.viewHomepageRequest',name="index" ),
    url( r'login', 'User.views.loginUserRequest',name="login" ),
    url( r'logout', 'User.views.logoutUser',name="logout" ),
    url( r'profile/edit', 'User.views.editProfile', name="profile/edit" ),
    url( r'profile/(?P<username>\w+)/$', 'User.views.viewProfile', name="profile" ),
    url( r'profile/', 'User.views.viewProfile',name="profile" ),
    url( r'register', 'User.views.registerNewUser',name="register" ),
    url( r'banned', 'User.views.registerNewUser', name="banned" ),
    url( r'deactivate', 'User.views.deactivateAccount', name="deactivate" ),
    url( r'forgotpassword', 'User.views.forgotPasswordRequest',name="forgotpassword" ),
 )
