from django.conf.urls import patterns, url

from User import views

urlpatterns = patterns( '',
    ( r'index/$', 'User.views.indexView.viewHomepage' ),
    ( r'login/', 'User.views.loginUserRequest' ),
    ( r'logout', 'User.views.logoutUser' ),
    ( r'profile/edit', 'User.views.editProfile' ),
    ( r'profile/(?P<username>\w+)/$', 'User.views.viewProfile' ),
    ( r'profile/', 'User.views.viewProfile' ),
    ( r'register', 'User.views.registerNewUser' ),
    ( r'banned', 'User.views.registerNewUser' ),
    ( r'deactivate', 'User.views.deactivateAccount' ),
    ( r'forgotpassword', 'User.views.forgotPasswordRequest' ),
 )
