from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from User.models import PongUser
from User.models import Institution

admin.site.register(Institution)

class PongUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = PongUser

class PongUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = PongUser

class PongUserAdmin(UserAdmin):
    form = PongUserChangeForm
    add_form = PongUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_banned',)}),
    )

admin.site.register(PongUser, PongUserAdmin)
