from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
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

    if not request.user.is_authenticated():
        state = "You are not logged in. Log in meow."
        return redirect_with_params('/login/', state=state)
     
    username = request.session['username']
    if request.method == 'POST':
        
        form = EditProfileForm(request.POST)
        if form.is_valid():
            
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            height = form.cleaned_data['height']
            institution = form.cleaned_data['institution']
            yearOfGradution = form.cleaned_data['graduation_year']
            userProfilePhoto = form.cleaned_data['photo']
            deactivate =   form.cleaned_data['deactivate']
            _updateUser(username,firstname,lastname,email,height,yearOfGradution,userProfilePhoto,deactivate)

            # Always redirect after a POST
            return redirect('profile/edit/')
        
        print("Form is not valid")
        
    else:
        # This the the first page load, display a blank form
        
        form = EditProfileForm()
    context = Context({'title': 'Edit Profile', 'form': form, 'username':username})

    return render(request,'user/editProfile.html',context)




def _updatePassword(password):
    
    return

def _updateUser(username,firstName,lastName,email,height,yearOfGradution,userProfilePhoto,deactivate):
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
    
    user = get_user_model().objects.get(username=username)
      
    user.setHeight(height)
    user.setGraduationYear(yearOfGradution)
    user.setPhoto(userProfilePhoto)
    user.setFirstName(firstName)
    user.setLastName(lastName)
    user.setEmail(email)
    user.setIsActive(deactivate)
    user.save()
    return



