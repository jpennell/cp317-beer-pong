from django.contrib.auth import *
from django import forms
from User.models import PongUser


class DeactivateAccountForm( forms.ModelForm ):
    """The form for deactivating an account,
        username -- The username of the account being deactivated
        password -- a password field for the user to confirm they 
        want to deactivate the account.
    Contributors:
        Quinton Black

    """
    username = forms.CharField( 
        widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'})
            )
    
    password = forms.CharField(
            max_length=250,
            widget = forms.PasswordInput(attrs={'placeholder':'password'})
            )


    def clean(self):
        """cleans the data in deactivate form
        -- ensures that the password belongs to the username
        
        Contributors:
            Quinton Black

        """
        
        cleaned_data = super(DeactivateAccountForm, self).clean()
        password = cleaned_data.get('password') 
        username = cleaned_data.get('username')
        if authenticate(username=username,password=password) is None:
            msg = u"Incorrect Password"   
            self._errors['password'] = self.error_class([msg]) 

        return cleaned_data
        