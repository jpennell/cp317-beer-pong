from django.conf.urls import patterns, url

from Statistics import views

urlpatterns = patterns('',
                       url(r'leaderboard/$','Statistics.views.leaderboardPage'),
                      )