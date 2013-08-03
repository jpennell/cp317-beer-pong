from django.shortcuts import render, redirect
from User.models import PongUser
from django.contrib import messages
from Statistics.views.leaderBoardView import *
from User.forms.profileForm import ProfileForm
from Utilities.game_utilities import obtainGamesToBeConfirmed

def viewProfile( request, username=None ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black
    Erin Cramer
    Matthew Hengeveld

    Output:

    """   
    
    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    form = ProfileForm()
    
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        
        if form.is_valid():
        
            username = form.cleaned_data['search']
        
            user = PongUser.objects.get(username=username)
            
            rank = getUserRank(user)
            instRank = getInstitutionRank(user)
            
            totalSunk = getTotalSunk(user.getLifeStats())
                   
            return render( request, 'user/profile.html', {'user':user, 'rank':rank, 'instRank':instRank, 'totalSunk':totalSunk, 'form':form} )
    
    if username is None:
        username = request.session['username']
    
    gamesToConfirm = obtainGamesToBeConfirmed(username)[0]
    if gamesToConfirm != []:
        messages.add_message(request,messages.INFO,"You have games that need to be <a href = '/game/verify'>verified</a>")
 
    user = PongUser.objects.get(username=username)

    rank = getUserRank(user)
    instRank = getInstitutionRank(user)
    
    totalSunk = getTotalSunk(user.getLifeStats())
           
    return render( request, 'user/profile.html', {'user':user, 'rank':rank, 'instRank':instRank, 'totalSunk':totalSunk, 'form':form} )
