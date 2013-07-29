from django import forms

class ForgotPasswordForm(forms.Form):
    """The form for sending a temporary password to the user if they have forgotten it,
        username -- The username of the account being deactivated
        email -- the email to send the message to
    Contributors:
        Quinton Black

    """
    username = forms.CharField( 
        max_length = 250,
        label = "Username",
        widget=forms.TextInput(attrs={'placeholder':'username'})
           )
    
    
    email = forms.EmailField( 
        max_length = 250,
        label = "Email address",
        widget = forms.TextInput( attrs = {'placeholder': 'email'} ),
        required = True,
    )
    
    

