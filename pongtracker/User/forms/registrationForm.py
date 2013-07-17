from django import forms

class RegistrationForm(forms.Form):
    
    email = forms.EmailField( 
            max_length = 250,
            label = "Email address",
            widget = forms.TextInput( attrs = {'placeholder': 'email'} )
        )
    
    username = forms.CharField( 
            max_length = 250,
            label = "Username",
            widget = forms.TextInput( attrs = {'placeholder': 'username'} )
        )
