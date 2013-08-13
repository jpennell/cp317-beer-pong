from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

from User.models import *


class PongUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = PongUser

class PongUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = PongUser
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
             PongUser._default_manager.get(username=username)
        except PongUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class PongUserAdmin(UserAdmin):
    form = PongUserChangeForm
    add_form = PongUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('_isBanned','_institution')}),
    )

admin.site.register(PongUser, PongUserAdmin)

