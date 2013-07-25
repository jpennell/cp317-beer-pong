from django.shortcuts import render, redirect
from User.models import PongUser

def viewProfile( request, username=None ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black
    Erin Cramer

    Output:

    """   
    if username == None:
        try:
            username = request.session['username']
        except KeyError:
            return redirect('/login/')
          
    user = PongUser.objects.get(username=username)
           
    return render( request, 'user/profile.html', {'user':user} )
