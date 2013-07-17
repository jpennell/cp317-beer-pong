from django import forms
import datetime
from User.models import Institution

class EditProfileForm( forms.Form ):
    year_choices = []

    for r in range( ( datetime.datetime.now().year ), ( datetime.datetime.now().year + 11 ) ):
        year_choices.append( ( r, r ) )

    year_tuple = ( year_choices )

    firstname = forms.CharField( 
        max_length = 250,
        label = "First name",
        widget = forms.TextInput( attrs = {'placeholder': 'first name'} )
    )

    lastname = forms.CharField( 
        max_length = 250,
        label = "Last name",
        widget = forms.TextInput( attrs = {'placeholder': 'last name'} )
    )

    email = forms.EmailField( 
        max_length = 250,
        label = "Email address",
        widget = forms.TextInput( attrs = {'placeholder': 'email'} )
    )

    height = forms.IntegerField( 
        max,
        label = "Height",
        widget = forms.TextInput( attrs = {'placeholder': 'height'} )
    )

    institution = forms.ModelChoiceField( 
        Institution.objects.all(),
        empty_label = "No institutions"
    )

    graduation_year = forms.ChoiceField( 
        choices = year_tuple,
        label = "Graduation Year"
    )

    photo = forms.ImageField( label = "Profile Photo" )

    deactivate = forms.BooleanField( label = "I would like to deactivate my account." )
