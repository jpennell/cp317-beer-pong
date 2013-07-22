from django.shortcuts import render, redirect,get_object_or_404
from User.models import PongUser
from django.shortcuts import redirect, render
from User.forms import EditProfileForm
from django.template import Context
from django.contrib.auth import get_user_model
from Utilities.utilities import *



def editProfile(request):
    """
    {{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    Erin Cramer
    
    Output:
        
    """
    state=""
    if not request.user.is_authenticated():
        state = "You are not logged in. Log in meow."
        return redirect_with_params('/login/', state=state)
     
    username = request.session['username']
    if request.method == 'POST':
        
        user = PongUser.objects.get(username=username)
        form = EditProfileForm(request.POST,instance=user)
        if form.is_valid():
            
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            height = form.cleaned_data['_height']
            institution = form.cleaned_data['_institution']
            yearOfGradution = form.cleaned_data['_graduationYear']
            userProfilePhoto = form.cleaned_data['_photo']
            deactivate =   form.cleaned_data['_deactivate']
            _updateUser(username,firstname,lastname,email,height,yearOfGradution,userProfilePhoto,deactivate,institution)

            # Always redirect after a POST
            request.session['updated']="Profile information has been updated"
            return redirect('edit/')
        
    else:
        # This the the first page load, display a form with the user filled
        
        user = PongUser.objects.get(username=username)
        form = EditProfileForm(instance=user)

        if 'updated' in request.session:
            state = request.session.pop('updated')

    context = Context({'title': 'Edit Profile', 'form': form, 'username':username,'updated':state})
    request.session

    return render(request,'user/editProfile.html',context)




def _updatePassword(password):
    
    return

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



