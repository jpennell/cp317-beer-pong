from django.shortcuts import render, redirect,get_object_or_404
from User.models import PongUser
from User.forms import deactivateAccountForm
from django.template import Context
from django.contrib.auth import *

from django.contrib import messages


def deactivateAccount(request):
    
        
    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit') 
    
    if request.POST():
        
        form = deactivateAccountForm(request.POST)
        if form.is_valid():
            username = form.cleanded_data['username']
            password = form.cleanded_data['password']
            _deactivateUser(username,password)
            messages.add_message(request,messages.SUCCESS,"Your account has been successfully deactivated. Hope your liver forgives you.")
            
            return redirect(request,'/logout')
        
    username = request.session['username']        
    user = PongUser.objects.get(username=username)
    form = deactivateAccountForm(instance=user)

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
    user = authenticate(username=username,password=password)
    if user is not None:
        user.setIsActive(False)
        user.save()
    return     
    