from django import forms
from User.models import PongUser

import re


class RegistrationForm(forms.Form):
    
    
    username = forms.CharField( 
            max_length = 30,
            label = "Username",
            widget = forms.TextInput( attrs = {'placeholder': 'username'} )
        )
    
    email = forms.EmailField( 
            max_length = 250,
            label = "Email address",
            widget = forms.TextInput( attrs = {'placeholder': 'email'} )
        )
    
    def clean_username(self):
            """Applys custom validation to username
            Adds errors if is not a valid username
            
            Keyword arguments:
            self -- data to be cleaned
            
            Contributors:
            Erin Cramer
            Quinton Black
                        
            Output:
            username -- the cleaned data
            """
            username = self.cleaned_data['username'] 
            match = re.search('[^A-Za-z0-9_.]',username)
            if match or len(username) > 30:
                msg = 'User name does not fit the format 30 characters or fewer. Letters, digits, _ and . only'
                self._errors['username'] = self.error_class([msg])

            return username
            
            
            
            