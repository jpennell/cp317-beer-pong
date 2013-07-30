from django import forms
from User.models import PongUser
import re

class CreateGameForm(forms.Form):
        
    #username fields
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
    
    #email fields
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
    
    #register checkboxes
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
    
    #suggested usernames
    suggestedUsernames2 =''
    suggestedUsernames3 =''
    suggestedUsernames4 =''
    
    
    def clean(self):
        """ validates all data from the form; sets error messages for appropriate field
            checks that - there are no duplicate usernames
                        - each user exists (if not registering)
                        - there are no banned users
                        - there are no inactive users
                        - a username is not taken (when registering)
                        - a valid email is entered (when registering)
    
        Keyword arguments:
        self      
        
        Contributors: 
        Matt Hengeveld
        Quinton Black
        
        Output:
        clean_data -- valid form data
                    
        """
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
        
        #Check that non to be registered users are not banned
        _checkUserBanned(usernameList[1:],self)
        
        #Check that non to be registered users are not inactive
        _checkUserInactive(usernameList[1:],self)
        
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
    """ checks database to see if users exist; does not check users that are registering;
        sets error messages for appropriate field

    Keyword arguments:
    usernameList -- list of users
    toRegisterUserList -- list of true/false determining if user needs to be registered  
    
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
    """ checks username for invalid characters when registering;
        sets error messages for appropriate field

    Keyword arguments:
    usernames -- list of usernames
    
    Contributors: 
    Matt Hengeveld
    
    Output: None
        
    """
    for x in range(len(usernames)):
        if usernames[x] is not None:
            match = re.search('[^A-Za-z0-9_.]',usernames[x])
            if match:
                msg = "Username must contain only the characters A-Z a-z 0-9 _ ."
                self._errors['username{0}'.format(x+2)] = self.error_class([msg])
            
    return 

def _checkUserBanned(usernames,self):
    """ checks if users are banned;
        sets error messages for appropriate field

    Keyword arguments:
    usernames -- list of usernames
    
    Contributors: 
    Matt Hengeveld
    
    Output: None
        
    """
    for x in range(len(usernames)):
        user = _findUser(usernames[x])
        banned = False
        try:
            banned = user.getIsBanned()
        except:
            pass
        if banned:
            msg = "User is banned"
            self._errors['username{0}'.format(x+2)] = self.error_class([msg])
            
    return

def _checkUserInactive(usernames,self):
    """ checks if users are inactive;
        sets error messages for appropriate field

    Keyword arguments:
    usernames -- list of usernames
    
    Contributors: 
    Matt Hengeveld
    
    Output: None
        
    """
    for x in range(len(usernames)):
        user = _findUser(usernames[x])
        active = True
        try:
            active = user.getIsActive()
        except:
            pass
        if not active:
            msg = "User is inactive"
            self._errors['username{0}'.format(x+2)] = self.error_class([msg])
            
    return

def _checkDuplicateUsernames(usernames,self):
    """ checks for duplicate usernames

    Keyword arguments:
    usernames -- list of usernames
    
    Contributors: 
    Matt Hengeveld
    Quinton Black
    
    Output: None
        
    """
    for x in range(len(usernames)):
        if usernames[x] is not None:
            if (usernames.count(usernames[x]) > 1):
                msg = 'Duplicate user'
                self._errors['username{0}'.format(x+1)] = self.error_class([msg])     
    return    

def _findUser(username):
    """ finds user in the database

    Keyword arguments:
    username -- string; username entered on form
    
    Contributors: Matt Hengeveld
    
    Output:    
    user -- user object; returns None is not found
        
    """
    user = None
    try:
        user = PongUser.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    finally:
        return user
    
    

 
    