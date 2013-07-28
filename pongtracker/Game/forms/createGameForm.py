from django import forms
from User.models import PongUser
import re

class CreateGameForm(forms.Form):
        
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username','class':'disabled', 'readonly':'readonly'}),
        label="Player 1",
        max_length=30)
    
    username2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username'}),
        label="Player 2",
        max_length=30)
    
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
    )
    
    chkRegister3 = forms.BooleanField( 
        label = "Register to play",
        required = False,
    )

    chkRegister4 = forms.BooleanField( 
        label = "Register to play",
        required = False,
    )

    
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
        
        #Check that usernames fit out format
        _checkUsernames(usernameList,self)
        #Check that no usernames are repeated
        _checkDuplicateUsernames(usernameList,self)
        #Check that non to be registered users exist
        userList=[]
        for username in usernameList:
            user =  _findUser(username)
            userList.append(user)
            
        _chkUsersExist(userList, toRegisterUserList,self)
        
        
                    
        
        return cleaned_data


def _checkUsernames(usernames,self):
    
    for x in range(len(usernames)):
        match = re.search('[^A-Za-z0-9_.]',usernames[x])
        if match:
            msg = "Username must contain only the characters A-Z a-z 0-9 _ ."
            self._errors['username{0}'.format(x)] = self.error_class([msg])
            
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
        if (usernames.count(usernames[x]) > 1):
            msg = 'Duplicate user'
            self._errors['username{0}'.format(x)] = self.error_class([msg])     
    return    


def _chkUsersExist(users, regUser, self):
    """checks database to see if users exist; does not check users that have 'register to play' checked

    Keyword arguments:
    users -- list of users
    regUser -- list of checkbox states (indicating 'register to play')
    
    Contributors: Matt Hengeveld
    
    Output: None
        
    """
    for x in range(len(users)):
        if regUser[x] is False:
            if users[x] is None:
                msg = "User not registered, please click register if you would like to claim that username"
                self._errors['username{0}'.format(x)] = self.error_class([msg])

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
    
    

 
    