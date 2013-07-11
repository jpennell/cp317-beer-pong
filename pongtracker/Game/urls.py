from django.conf.urls import patterns, url

from Game import views

urlpatterns = patterns('',
                       url(r'create/$','Game.views.createNewGameRequest'),
                       url(r'(?P<game_id>\d+)/$','Game.views.getGame'),
)