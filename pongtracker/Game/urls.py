from django.conf.urls import patterns, url

from Game import views

urlpatterns = patterns('',
                       url(r'create/$','Game.views.createNewGameRequest'),
                       url(r'(?P<game_id>\d+)/play/$','Game.views.scoreGame'),
                       url(r'verify/$','Game.views.verifyGameRequest'),
                       url(r'(?P<game_id>\d+)/confirm/$', 'Game.views.confirmGame'),
                       url(r'(?P<game_id>\d+)/deny/$', 'Game.views.denyGame'),
                       url(r'(?P<game_id>\d+)/summary/$','Game.views.viewGameSummaryRequest'),
                       url(r'(?P<game_id>\d+)/info/$','Game.views.infoGameRequest'),

)