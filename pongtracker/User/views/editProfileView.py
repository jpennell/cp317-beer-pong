from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from User.forms import EditProfileForm



def editProfile( request ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black

    Output:

    """
    form = EditProfileForm()
    context = Context({'title': 'Add Item', 'form': form})
    
    return render(request,'user/editProfile.html',context)




def _updatePassword( password ):

    return

def _updateUser( username, password, firstName, lastName, email, height, yearOfGradution, userProfilePhoto, isBanned ):



    return



