from django.shortcuts import render, redirect,get_object_or_404
from User.models import PongUser
from User.forms import DeactivateAccountForm
from django.template import Context
from django.contrib.auth import *
from django.conf import settings
from django.contrib import messages


def deactivateAccount(request):
    """Processes a request whenever a  brower is sent to deactivate the account
    Keyword arguments:
        request -- The request sent to the url
        
    Contributors:
    Quinton Black
    
    Output:
        HTTPRESPONSE -- either a redirect or a render
    """
        
    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect(settings.SITE_URL+'login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect(settings.SITE_URL+'profile/edit') 
    
    username = request.session['username']        
    user = PongUser.objects.get(username=username)

    if request.method=='POST':
        
        form = DeactivateAccountForm(request.POST,instance=user)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            _deactivateUser(username,password)
            messages.add_message(request,messages.SUCCESS,"Your account has been successfully deactivated. Hope your liver forgives you.")
            
                       
            return redirect(settings.SITE_URL+'logout')
    
    else:
        form = DeactivateAccountForm(instance=user)

    context = ({'title':'Deactivate Account','form':form})
    return render(request,'user/deactivateAccount.html',context)



def _deactivateUser(username,password):
    """Checks to see if the User has correctly entered their password by calling Django's authenticate function.
    If so, the Users account is deactivated.
    Keyword arguments:
        username -- The current user's username
        password -- the users password
        
    Contributors:
    Quinton Black
    
    Output:
        None
    """
    print("Deactivating user with username: {0} and password {1}".format(username,password))
    
    user = authenticate (username=username,password=password)
    if user is not None:
        user.setIsActive(False)
        user.save()
    return     
    