from Game.models import Game, Event, EventType
from django.shortcuts import render, redirect
from Utilities.utilities import *
from User.models import PongUser

def scoreGame(request, game_id):
       
    if not request.user.is_authenticated():
        messages.add_message(request,message.INFO,'Please Login')
        return redirect('/login/')
     
    if not request.user.getHasUpdatedProfile():
        messages.add_message(request,messages.INFO,'Please edit your profile before continuing')
        return redirect('/profile/edit')
    
    #need to get username from the post since it isn't necessarily going to be the user logged in the event is logged against
    username = request.POST['username']
    
    game = Game.objects.get(pk=game_id)
    
    #why is this here? only need one user for an event
    users = [game.getTeam1().getUser1(), game.getTeam1().getUser2(), game.getTeam2().getUser1(), game.getTeam2().getUser2()]
    
    #get the info we need
    if request.method == 'POST':

        eventTypeName = request.POST['eventType']
        
        eventType = EventType.objects.get(_typeName=eventTypeName)
        user = PongUser.objects.get(username=username)
        
        if eventTypeName == 'Undo':
            
            event = _undoEvent()
            
        else:
            #create event
            event = Event.objects.create(_game=game, _eventType=eventType, _user=user, _cup1=True, _cup2=False, _cup3=False, _cup4=False, _cup =False, _cup6=False)
    
    return render(request, 'game/play.html', {'users': users})      
    #not sure what to render/redirect to if it even needs to happen
    
    
def _undoEvent(game):
        """Undo the previous event

        Keyword arguments:
        gameID -- current game (int)
        
        
        Contributors:
        Erin Cramer
        
        Output:
        current_status - event before the one undone (Event)
        
        """
        
        game_events = game.Events.all()
        last_event = game_events[len(game_events)-1]
        last_event.delete()
        current_status = game_events[len(game_events)-2]
        
        return current_status