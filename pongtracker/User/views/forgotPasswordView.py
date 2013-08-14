from django.shortcuts import render, redirect
from User.models import PongUser
from django.contrib import messages
from django.template import Context
from django.core.mail import send_mail, BadHeaderError
from User.forms import ForgotPasswordForm
from Utilities.utilities import *
from django.conf import settings

def forgotPasswordRequest(request):
    
    if request.user.is_authenticated():
        msg = 'You are already logged in'
        messages.add_message(request,messages.WARNING,msg)
        return redirect(settings.SITE_URL+'index/')
    
    if request.method =='POST':
        
        form = ForgotPasswordForm(request.POST)
    
        if form.is_valid():
            
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = _getUserByEmail(username,email)
            
            if user is None:
                msg = 'There is no account registered with that email'
                messages.add_message(request,messages.WARNING,msg)
                
                context =Context( {'title':'Forget Me Not','form':form})
                return redirect(settings.SITE_URL+'forgotpassword',context)
            
            new_password = generatePassword()

            message = """
                Hello {0},
                
                I heard you don't remember much of the other night.
                I've changed your password for you. It is now {1}.
                Please login and change it to something, while in a
                remembering state of mind this time, please.

            """.format(username,new_password)
            sendEmail(username, email, new_password,message)
            user.set_password(new_password)
            user.setHasUpdatedProfile(False)
            user.save()
            msg = 'A temporary password has been sent to your email.'
            messages.add_message(request,messages.SUCCESS,msg)
            return redirect(settings.SITE_URL+'index') 
        
        context = Context({'title':'Forget Me Not','form':form})
        return render(request,'user/forgotPassword.html',context)
    
    
    form = ForgotPasswordForm()
    context = Context({'title':'Forget Me Not','form':form})
    return render(request,'user/forgotPassword.html',context)
 
def _getUserByEmail(username,email):
    """ Finds the user opject based upon username and email
   
    Keyword arguments:
        username -- The current user's username (String)
        email --  The emial of the user (String)
       
    Contributors:
    Quinton Black
    
    Output:
        user - the user that the email belongs to (User), 
        None if the user does not exist
    """
    try:
         user = PongUser.objects.get(username=username,email=email)
    except:
        user = None
    
    return user
