from django import forms
import datetime
from User.models import Institution

class EditProfileForm( forms.ModelForm ):
    year_choices = []

    for r in range( ( datetime.datetime.now().year ), ( datetime.datetime.now().year + 11 ) ):
        year_choices.append( ( r, r ) )

    year_tuple = ( year_choices )

    first_name = forms.CharField( 
        max_length = 250,
        label = "First name",
        widget = forms.TextInput( attrs = {'placeholder': 'first name'} ),
        required = True,
            )

    last_name = forms.CharField( 
        max_length = 250,
        label = "Last name",
        widget = forms.TextInput( attrs = {'placeholder': 'last name'} ),
        required = True,
    )

    email = forms.EmailField( 
        max_length = 250,
        label = "Email address",
        widget = forms.TextInput( attrs = {'placeholder': 'email'} ),
        required = True,
    )

    _height = forms.IntegerField( 
        max,
        label = "Height",
        widget = forms.TextInput( attrs = {'placeholder': 'height'} ),
        required = True,
    )

    _institution = forms.ModelChoiceField( 
        queryset=Institution.objects.all(),
        required = True,
        label = "Institution"
    )

    _graduationYear = forms.ChoiceField( 
        choices= year_choices,
        label = "Graduation Year",
        required = True,
    )

    _photo = forms.ImageField( label = "Profile Photo", required = False )

    _deactivate = forms.BooleanField( 
        label = "I would like to deactivate my account.",
        required = False,
    )
