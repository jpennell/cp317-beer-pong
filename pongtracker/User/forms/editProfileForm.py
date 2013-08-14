from django.contrib.auth import *
from django import forms
import datetime
from User.models import Institution, PongUser

MIN_HEIGHT =100
MAX_HEIGHT = 300


class EditProfileForm( forms.ModelForm ):
    year_choices = []

    for r in range( ( datetime.datetime.now().year ), ( datetime.datetime.now().year + 6 ) ):
        year_choices.append( ( r, r ) )

    
    username = forms.CharField( 
        widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'})
            )

    first_name = forms.CharField( 
        max_length = 250,
        label = "First name *",
        widget = forms.TextInput( attrs = {'placeholder': 'first name'} ),
        required = True,
            )

    last_name = forms.CharField( 
        max_length = 250,
        label = "Last name *",
        widget = forms.TextInput( attrs = {'placeholder': 'last name'} ),
        required = True,
    )

    email = forms.EmailField( 
        max_length = 250,
        label = "Email address *",
        widget = forms.TextInput( attrs = {'placeholder': 'email'} ),
        required = True,
    )

    _height = forms.IntegerField( 
        label = "Height *",
        widget = forms.TextInput( attrs = {'placeholder': 'height in cm'} ),
        required = True,
    )

    _institution = forms.ModelChoiceField( 
        queryset=Institution.objects.all(),
        required = True,
        label = "Institution *"
    )

    _graduationYear = forms.ChoiceField( 
        choices= year_choices,
        label = "Graduation Year *",
        required = True,
    )

    _photo = forms.ImageField( label = "Profile Photo", required = False )

    _deactivate = forms.BooleanField( 
        label = "I would like to deactivate my account.",
        required = False,
    )
    
    
    oldPassword = forms.CharField( 
        max_length = 250,
        label = "Old Password",
        widget = forms.PasswordInput,
        required = False,
            )

    newPassword = forms.CharField( 
        max_length = 250,
        label = "New Password",
        widget = forms.PasswordInput,
        required = False,
            )
    confirmPassword = forms.CharField( 
        max_length = 250,
        label = "Confirm Password",
        widget = forms.PasswordInput,
        required = False,
            )
    
    _hasUpdatedProfile = forms.BooleanField(
        label='',
        widget = forms.HiddenInput(),
        required = False,
        )
    
    _hasAcceptedTerms = forms.BooleanField( 
        label = '',
        required = False,
        widget = forms.CheckboxInput(attrs = {'style':'display:none'}), 
            )


    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()
        newPassword = cleaned_data.get('newPassword')
        confirmPassword = cleaned_data.get('confirmPassword')
        oldPassword = cleaned_data.get('oldPassword') 
        username = cleaned_data.get('username')
        hasUpdatedProfile =  cleaned_data.get('_hasUpdatedProfile')
        hasAcceptedTerms = cleaned_data.get('_hasAcceptedTerms')    
        height = cleaned_data.get('_height')
            
        if newPassword and confirmPassword and newPassword!=confirmPassword:
            msg = u"Passwords don't match"
            self._errors['confirmPassword'] = self.error_class([msg])
            
        if confirmPassword and newPassword and not oldPassword:
             msg = u"Please provide your old password"
             self._errors['oldPassword'] = self.error_class([msg])    
        
        if hasUpdatedProfile is False and not oldPassword:
            msg = "Please change your temporary password"
            self._errors['oldPassword'] = self.error_class([msg])
                
        
        if oldPassword:
            if authenticate(username=username,password=oldPassword) is None:
                 msg = u"Incorrect Password, note copy and paste does not work."   
                 self._errors['oldPassword'] = self.error_class([msg])
            if  not confirmPassword and not newPassword:
                msg = u'Please provide a new password'
                self._errors['newPassword'] = self.error_class([msg])
        
        #if hasUpdatedProfile is False and hasAcceptedTerms is False:
            #msg = u"We are not responsible for your liver, please accept the terms and conditions."  
            #self._errors['_hasAcceptedTerms'] = self.error_class([msg]) 
        
        if height < MIN_HEIGHT:
            msg = u"You must be at least {0}cm to play this game.".format(MIN_HEIGHT)   
            self._errors['_height'] = self.error_class([msg]) 
            
        elif height > MAX_HEIGHT:
            msg = u"Stilts are dangerous while intoxicated please remove them."   
            self._errors['_height'] = self.error_class([msg])
        
        
                
    
        return cleaned_data
    
