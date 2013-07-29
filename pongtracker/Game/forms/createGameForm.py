from django import forms
from User.models import PongUser
import re

class CreateGameForm(forms.Form):
        
    username1 = forms.CharField(
        widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'}),
        label="Player 1",
        max_length=30)
    
    username2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username'}),
        label="Player 2",
        max_length=30,
        required = True)
    
    username3 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username'}),
        label="Player 3",
        max_length=30)
    
    username4 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username'}),
        label="Player 4",
        max_length=30)
    
    email2 = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'}),
        label="Email",
        max_length=40,
        required = False)
    
    email3 = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'}),
        label="Email",
        max_length=40,
        required = False)
    
    email4 = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'}),
        label="Email",
        max_length=40,
        required = False)
    
    chkRegister2 = forms.BooleanField( 
        label = "Register to play",
        required = False,
        widget = forms.CheckboxInput(attrs={'onclick':"toggle_more2();"}), 
    )
    
    chkRegister3 = forms.BooleanField( 
        label = "Register to play",
        required = False,
        widget = forms.CheckboxInput(attrs={'onclick':"toggle_more3();"}), 
    )

    chkRegister4 = forms.BooleanField( 
        label = "Register to play",
        required = False,
        widget = forms.CheckboxInput(attrs={'onclick':"toggle_more4();"}), 
    )
    
    suggestedUsernames2 =''
    suggestedUsernames3 =''
    suggestedUsernames4 =''
    
    def clean(self):
    
        
        cleaned_data = super(CreateGameForm, self).clean()
        username1 = cleaned_data.get('username1')
        username2 = cleaned_data.get('username2')
        username3 = cleaned_data.get('username3')
        username4 = cleaned_data.get('username4')
        email2 = cleaned_data.get('email2')
        email3 = cleaned_data.get('email3')
        email4 = cleaned_data.get('email4')
        chkRegister2 = cleaned_data.get('chkRegister2')
        chkRegister3 = cleaned_data.get('chkRegister3')
        chkRegister4 = cleaned_data.get('chkRegister4')
        
        
        usernameList = [username1,username2,username3,username4]
        toRegisterUserList = [False,chkRegister2,chkRegister3,chkRegister4]

        #Check that no usernames are repeated
        _checkDuplicateUsernames(usernameList,self)
        #Check that non to be registered users exist
                
        _checkUserExists(usernameList[1:],toRegisterUserList[1:],self)
        
        #Check that usernames fit out format
        _checkUsernames(usernameList[1:],self)
        
        if chkRegister2 and not email2:
            msg = "A valid email is required"
            self._errors['email2'] = self.error_class([msg])
        
        if chkRegister3 and not email3:
            msg = "A valid email is required"
            self._errors['email3'] = self.error_class([msg])
        
        if chkRegister4 and not email4:
            msg = "A valid email is required"
            self._errors['email4'] = self.error_class([msg])

        return cleaned_data

def _checkUserExists(usernameList,toRegisterUserList,self):
    """checks database to see if users exist; does not check users that have 'register to play' checked

    Keyword arguments:
    users -- list of users
    
    
    Contributors: 
        Matt Hengeveld
    
    Output: None
        
    """
    index = 0
    for username in usernameList:
        if username is not None and toRegisterUserList[index] == False:
            user = _findUser(username)
            if user is None:
                msg = "Username not registered, please click register if you would like to claim that username"
                self._errors['username{0}'.format(index+2)] = self.error_class([msg])

        index+=1
    return
        
def _checkUsernames(usernames,self):
    for x in range(len(usernames)):
        if usernames[x] is not None:
            match = re.search('[^A-Za-z0-9_.]',usernames[x])
            if match:
                msg = "Username must contain only the characters A-Z a-z 0-9 _ ."
                self._errors['username{0}'.format(x+2)] = self.error_class([msg])
            
    return 



def _checkDuplicateUsernames(usernames,self):
    """checks for duplicate usernames

    Keyword arguments:
    usernames -- list of strings; usernames entered on form
    
    Contributors: 
        Matt Hengeveld
        Quinton Black
    
    Output:     False if no duplicates
                True if duplicates
        
    """
    for x in range(len(usernames)):
        if usernames[x] is not None:
            if (usernames.count(usernames[x]) > 1):
                msg = 'Duplicate user'
                self._errors['username{0}'.format(x+1)] = self.error_class([msg])     
    return    

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
    
    

 
    