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

    username = request.session['username']

    game = Game.objects.get( pk = game_id )
    users = [game.getTeam1().getUser1(),
             game.getTeam1().getUser2(),
             game.getTeam2().getUser1(),
             game.getTeam2().getUser2()]

    # get the info we need
    if request.method == 'POST':
        eventTypeName = request.POST['eventType']
        eventType = EventType.objects.get( _typeName = eventTypeName )
        user = PongUser.objects.get( username = username )
        if eventTypeName == 'undo':
            event = _undoEvent()
        else:
            # create event
            cups = []
            for i in range( 1, 7 ):
                cups.append( request.POST["cup" + i] )
            event = Event.objects.create( _game = game, _eventType = eventType, _user = user,
                                          _cup1 = cups[1], _cup2 = cups[2], _cup3 = cups[3],
                                          _cup4 = cups[4], _cup5 = cups[5], _cup6 = cups[6] )

    return render( request, 'game/play.html', {'users': users} )
    # not sure what to render/redirect to if it even needs to happen


def _undoEvent( game ):
        """Undo the previous event

        Keyword arguments:
        gameID -- current game (int)


        Contributors:
        Erin Cramer

        Output:
        current_status - event before the one undone (Event)

        """

        game_events = game.Events.all()
        last_event = game_events[len( game_events ) - 1]
        last_event.delete()
        current_status = game_events[len( game_events ) - 2]

        return current_status
