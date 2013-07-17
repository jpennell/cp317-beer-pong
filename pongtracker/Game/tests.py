from django.db import models

from django.test import TestCase
from mock import MagicMock#, call

from Game.views.createGameView import _createNewGame
from Game.models import PongUser, Team, Game

class SimpleTest(TestCase):

    def setUp(self):
        self.mockGame = MagicMock(spec=Game)

        self.mockUser1 = MagicMock(spec=PongUser)
        self.mockUser2 = MagicMock(spec=PongUser)
        self.mockUser3 = MagicMock(spec=PongUser)
        self.mockUser4 = MagicMock(spec=PongUser)

        self.mockTeam1 = MagicMock(spec=Team)
        self.mockTeam2 = MagicMock(spec=Team)

        self.mockTeams = [self.mockTeam1, self.mockTeam2]

    def tearDown(self):
        pass

    def testCreateGame(self):

        Team.objects.create = MagicMock(side_effect=self.returnTeams)
        Game.objects.create = MagicMock(return_value=self.mockGame)

        resultGame = _createNewGame(self.mockUser1, self.mockUser2, self.mockUser3, self.mockUser4)

        self.assertEqual(resultGame, self.mockGame)

        expected = [call(user1=self.mockUser1, user2=self.mockUser2), call(user1=self.mockUser3, user2=self.mockUser4)]
        self.assertTrue(Team.objects.create.call_args_list == expected)

        Game.objects.create.assert_called_with(team1=self.mockTeam1, team2=self.mockTeam2)

    def returnTeams(self, *args, **kwargs):
        return self.mockTeams.pop(0)
