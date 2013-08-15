from django import forms
from User.models import PongUser

class ProfileForm(forms.Form):
    """ The search box for profile
    
    Contributors:
        Quinton Black

    """
    search = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'search for player'}),
        label="User Search",
        max_length=30,
        required = True)
    
    
    def clean_search(self):
        username = self.cleaned_data['search']
        
        #Check that non to be registered users are not inactive
        if not _checkUserInactive(username,self):
            msg = "User inactive"
            self._errors['search'] = self.error_class([msg])
        
        #Check that non to be registered users exist
        exists = _checkUserExists(username,self)
        if not exists:
            msg = "No such user"
            self._errors['search'] = self.error_class([msg])
        
        return username

def _checkUserExists(username,self):
    """ checks that the user exists
    
    Keyword arguments:
    username -- the username to test against
    
    Contributors:
        Quinton Black
         
    Output:
        exists -- True or False depending on the user's existance 

    """
    
    exists = False
    
    if _findUser(username) is not None:
        exists = True
        
    return exists


def _checkUserInactive(username,self):
    """ checks that the user is active
    
    Keyword arguments:
    username -- the username to test against
    
    Contributors:
        Quinton Black
         
    Output:
        active -- True or False depending on the user's activness 

    """
    active = False
    user = _findUser(username)
    
    if user is not None:
        active = user.getIsActive()
    
    return active
    
    
def _findUser(username):
    """finds user in the database

    Keyword arguments:
    username -- string; username entered on form
    
    Contributors: Matt Hengeveld
    
    Output:    user object; returns None is not found
        
    """
    user = None
    try:
        user = PongUser.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    finally:
        return user