from django.db import models
import unittest
from django.test import TestCase
from mock import MagicMock#, call
from Game.views  import createGameView
from Game.models import PongUser, Team, Game

from django.test.utils import setup_test_environment
setup_test_environment()
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

#    def test_CreateGame(self):
#
#        Team.objects.create = MagicMock(side_effect=self.returnTeams)
#        Game.objects.create = MagicMock(return_value=self.mockGame)
#
#        resultGame = _createNewGame(self.mockUser1, self.mockUser2, self.mockUser3, self.mockUser4)
#
#        self.assertEqual(resultGame, self.mockGame)
#
#        expected = [call(user1=self.mockUser1, user2=self.mockUser2), call(user1=self.mockUser3, user2=self.mockUser4)]
#        self.assertTrue(Team.objects.create.call_args_list == expected)
#
#        Game.objects.create.assert_called_with(team1=self.mockTeam1, team2=self.mockTeam2)
        
    def test_chkBlank_withBlankArray(self):
         """ Check to see if blank names return True """
         blankNames = ['','','','']
         resultBlank = createGameView._chkBlank(blankNames)
         self.assertTrue(resultBlank)
         
    def test_chkBlank_withNonBlankArray(self):
         """ Check to see if non-blank names return False """
         nonBlankNames = ['test','test','test','test']
         resultNonBlank = createGameView._chkBlank(nonBlankNames)
         self.assertFalse(resultNonBlank)

    def test_chkBlank_withEmptyArray(self):
         """ Check to see if empty array returns true """
         empty = []
         resultNonBlank = createGameView._chkBlank(empty)
         self.assertFalse(resultNonBlank)

    
    def test_chkDup_withDuplicates(self):
         """ Check to see if duplicate names returns errors """
         dupNames = ['test','test','test1','test2']
         errList=['','','','']
         resultDup = createGameView._chkDup(dupNames,errList)
         self.assertDoesNotContain("Duplicate user",errList)
         
    def test_chkDup_withNoDuplicates(self):     
         """ Check to see if duplicate names return no errors """
         nonDupNames = ['test1','test2','test3','test4']
         errList=['','','','']
         resultDup = createGameView._chkDup(nonDupNames,errList)
         self.assertEqual(0,len(errList))


    def returnTeams(self, *args, **kwargs):
        return self.mockTeams.pop(0)
    
if __name__ == "__main__":
    
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

