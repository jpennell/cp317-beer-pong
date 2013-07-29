from django.shortcuts import render, redirect,get_object_or_404
from User.models import PongUser
from User.forms import EditProfileForm
from django.template import Context
from Utilities.utilities import *
from django.contrib.auth import *

from django.contrib import messages
from pickle import FALSE


def editProfile(request):
    """Proccess a request to the profile/edit

    Keyword arguments:
    request -- the request sent to the funciton 
       
    Contributors:
    Quinton Black
    Erin Cramer
    
    Output:
        HTTPResponse -- The page to redirect or render
    """

    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
     
    username = request.session['username']
    if request.method == 'POST':
        
        user = PongUser.objects.get(username=username)
        form = EditProfileForm(request.POST,instance=user)
      
        
        if form.is_valid():
           
            #Handle password change if password is correct 
            passwordChanged = False
            newPassword = form.cleaned_data['confirmPassword']
            oldPassword = form.cleaned_data['oldPassword']
            changingUser = authenticate(username=username,password=oldPassword)           
            if changingUser is not None:
                user.set_password(newPassword)
                user.save()
                msg="Your Password has been changed"
                messages.add_message(request,messages.SUCCESS,msg)
                passwordChanged =True   
            
            #Handle rest of form change 
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            height = form.cleaned_data['_height']
            institution = form.cleaned_data['_institution']
            yearOfGradution = form.cleaned_data['_graduationYear']
            userProfilePhoto = form.cleaned_data['_photo']
            deactivate = form.cleaned_data['_deactivate']
            termsAndConditions = form.cleaned_data['_hasAcceptedTerms']
            
            _updateUser(username,firstname,lastname,email,height,yearOfGradution,userProfilePhoto,deactivate,institution)
           
            #Declare that user has updated profile and password
            user.setHasUpdatedProfile(True)
            user.save()
            
            if deactivate:
                return redirect('/deactivate')
            
            
            messages.add_message(request,messages.SUCCESS,"Profile information has been updated")
            return redirect('edit/')
        else:
            if user.getHasUpdatedProfile() is False:
                form.fields['_hasAcceptedTerms'].label = 'I have read and agreed to the terms and conditions'
                form.fields['_hasAcceptedTerms'].widget.attrs['style'] =''
            
    else:
        # This the the first page load, display a form with the user filled
        
        user = PongUser.objects.get(username=username)

        
        form = EditProfileForm(instance=user)
        if user.getHasUpdatedProfile() is False:
            form.fields['_hasAcceptedTerms'].label = 'I have read and agreed to the terms and conditions'
            form.fields['_hasAcceptedTerms'].widget.attrs['style'] =''

    context = Context({'title': 'Edit Profile', 'form': form, 'username':username})

    return render(request,'user/editProfile.html',context)

def _updateUser(username,firstName,lastName,email,height,yearOfGradution,userProfilePhoto,deactivate,institution):
    """Updates a user with the values provided

    Keyword arguments:
        username -- The current user's username
        firstName --The first name to be set
        lastName --  The last name to be set
        email --  The emial to be set 
        height -- The height to be set 
        yearOfGradution --  The year of graduation to be set
        userProfilePhoto --  The desired profile photo to be set
        deactivate --  Whether to deactivate the user or not
        
    Contributors:
    Quinton Black
    
    Output:
        None
        
    """

    user = PongUser.objects.get(username=username)
    user.setHeight(height)
    user.setGraduationYear(yearOfGradution)
    user.setPhoto(userProfilePhoto)
    user.setFirstName(firstName)
    user.setLastName(lastName)
    user.setEmail(email)
    user.setIsActive(deactivate)
    user.setInstitution(institution)
    user.save()
    return



