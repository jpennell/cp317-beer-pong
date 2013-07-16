from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from User.models import PongUser
from User.models import Institution

admin.site.register(Institution)
## Define an inline admin descriptor for UserProfile model
## which acts a bit like a singleton
#class ProfileInline(admin.StackedInline):
#    model = PongUser
#    can_delete = False
#    verbose_name_plural = 'profile'
#
## Define a new User admin
#class UserAdmin(UserAdmin):
#    inlines = (ProfileInline, )
#
## Re-register UserAdmin
admin.site.register(PongUser)
#admin.site.register(User, UserAdmin)