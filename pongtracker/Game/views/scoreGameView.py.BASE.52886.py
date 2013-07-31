from Game.models import Game, Event, EventType
from django.shortcuts import render, redirect
from Utilities.utilities import *
from User.models import PongUser

def scoreGame( request, game_id ):
    """Creates and undoes events

    Keyword arguments:
    gameID -- current game (int)


    Contributors:
    Quinton Black
    Erin Cramer
    George Lifchits

    Output:
    current_status - event before the one undone (Event)

    """
    if not request.user.is_authenticated():
        messages.add_message( request, message.INFO, 'Please Login' )
        return redirect( '/login/' )

    if not request.user.getHasUpdatedProfile():
        messages.add_message( request, messages.INFO, 'Please edit your profile before continuing' )
        return redirect( '/profile/edit' )

    game = Game.objects.get( pk = game_id )

    # get the info we need
    if request.method == 'POST':
        
        eventTypeName = request.POST['eventType']
        
        
        if eventTypeName == 'undo':
            
           success = _undoEvent(game)
            
        else:
            # create event
            cup = request.POST['cup']
            cup2 = request.POST.get( 'cup2' )
            user_number = int(request.POST['player'])
            team = request.POST['team']
            eventType = EventType.objects.get( _typeName = eventTypeName )
            
            team = int(team[-1])
            user = game.getTeam(team).getUser(user_number)
            
            # initialize cups to a list of 6 False
            cups = [False] * 6
            # cup = "cupX", cup[-1] = "X"
            # make cup X true
            cups[int( cup[-1] )] = True
            
            if cup2:
                cups[int( cup2[-1] )] = True

            event = Event.objects.create( _game = game, _eventType = eventType, _user = user,
                                          _cup1 = cups[0], _cup2 = cups[1], _cup3 = cups[2],
                                          _cup4 = cups[3], _cup5 = cups[4], _cup6 = cups[5] )

    return render( request, 'game/play.html', {'game': game} )
    # not sure what to render/redirect to if it even needs to happen


def _undoEvent( game ):
        """Undo the previous event

        Keyword arguments:
        gameID -- current game (int)


        Contributors:
        Erin Cramer

        """
        try:
            game_events = game.getEvents()
            last_event = game_events[-1]
            last_event.delete()
            success = True
        except:
            success = False
        
        return success
