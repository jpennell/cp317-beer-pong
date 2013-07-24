from django.shortcuts import render

def viewProfile( request, username ):
    """{{Description}}

    Keyword arguments:
    variable -- description
    variable -- description

    Contributors:
    Quinton Black

    Output:

    """   
    
    if username == None:
        try:
            username = request.session['username']
        except KeyError:
            redirect('/login/')
            
    user = PongUser.objects.get(username=username)       
    return render( request, 'user/profile.html', {'user':user} )
