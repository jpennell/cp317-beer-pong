from Game.models import Game, Event, EventType
from django.shortcuts import render, redirect
from Utilities.utilities import *
from User.models import PongUser
from django.conf import settings

def scoreGame( request, game_id ):
    """
    Creates and undoes events by handling POST requests from the client end

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
        return redirect( settings.SITE_URL+'login/' )

    if not request.user.getHasUpdatedProfile():
        messages.add_message( request, messages.INFO, 'Please edit your profile before continuing' )
        return redirect(settings.SITE_URL+ 'profile/edit' )

    game = Game.objects.get( pk = game_id )

    # get the info we need
    if request.method == 'POST':
        print( "I am getting a post" )
        print request.POST
        eventTypeName = request.POST['eventType']

        if eventTypeName == 'undo':
            try:
                _undoEvent( game )
            except Exception, e:
                print "undo failed: %s" % e

        else:
            # create event
            eventTypeString = request.POST.get( 'eventType' )
            cup = request.POST.get( 'cup' )
            cup2 = request.POST.get( 'cup2' )
            user_number = int( request.POST.get( 'player', 0 ) )
            team = request.POST.get( 'team' )
            eventType = EventType.objects.get( _typeName = eventTypeName )

            if eventTypeString == 'death':
                pass

            if team:
                team = int( team[-1] )

            user = game.getTeam( team ).getUser( user_number )

            # initialize cups to a list of 6 False
            cups = [False] * 6
            # cup = "cupX", cup[-1] = "X"
            # make cup X true
            if cup:
                cups[int( cup[-1] ) - 1] = True

            if cup2:
                cups[int( cup2[-1] ) - 1] = True

            event = Event.objects.create( _game = game, _eventType = eventType, _user = user,
                                          _cup1 = cups[0], _cup2 = cups[1], _cup3 = cups[2],
                                          _cup4 = cups[3], _cup5 = cups[4], _cup6 = cups[5] )
            
            if eventTypeName == 'win':
                return redirect(settings.SITE_URL+'game/'+game_id+'/summary') #does not work; needs to redirect to summary.html page on win event

    return render( request, 'game/play.html', {'game': game} )
    # not sure what to render/redirect to if it even needs to happen


def _undoEvent( game ):
    """Undo the previous event

    Keyword arguments:
    gameID -- current game (int)


    Contributors:
    Erin Cramer
    George Lifchits

    """
    print 'undo event called'
    last_event = game.getLastEvent()
    last_event.delete()

