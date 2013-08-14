from django.shortcuts import render

def bannedView(request):
    """{{Description}}

    Keyword arguments:
    variable -- description 
    variable -- description 
    
    Contributors:
    Quinton Black
    Erin Cramer
    
    Output:
        
    """
    
    username = request.POST.get('username','')
    
    render(request, 'user/banned.html', {'username':username})