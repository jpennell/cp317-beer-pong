/*
 * score.js
 *
 * George Lifchits
 * July-August 2013
 *
 * JavaScript code which implements the Score Game aspect of the Pong Tracker project
 *
 *
 *
 */
game = {
	/* global game variable */
	'isOver' : false,
	'team1' : {
		1 : 'Team 1, Player 1',
		2 : 'Team 1, Player 2',
		'cups' : {
			1 : false,
			2 : false,
			3 : false,
			4 : false,
			5 : false,
			6 : false
		}
	},
	'team2' : {
		1 : 'Team 2, Player 1',
		2 : 'Team 2, Player 2',
		'cups' : {
			1 : false,
			2 : false,
			3 : false,
			4 : false,
			5 : false,
			6 : false
		}
	}
}
/*
 *
 * functions
 *
 */
var deactivateCup = function(team, cup) {
	/* makes a cup deactive (by removing CSS class 'active) */
	if ( typeof cup == 'number')
		cup = 'cup' + cup
	if ( typeof team == 'number')
		team = 'team' + team
	var selector = '.' + team + '.' + cup
	if ($(selector).hasClass('active')) {
		console.debug('deactivating cup ' + selector)
		$(selector).removeClass('active')
		refreshUndo()
	}
}
var activateCup = function(team, cup) {
	/* makes a cup active (by adding CSS class 'active) */
	if ( typeof cup == 'number')
		cup = 'cup' + cup
	if ( typeof team == 'number')
		team = 'team' + team
	var selector = '.' + team + '.' + cup
	if (!$(selector).hasClass('active')) {
		console.debug('activating cup ' + selector)
		$(selector).addClass('active')
		refreshUndo()
	}
}
var refreshUndo = function() {
	/*
	 * refreshes the disabled status of the undo button
	 */
	var undoBtn = '[name="undo"]'
	if ($('.cups span.active').length == 12)
		$(undoBtn).attr('disabled', true)
	else
		$(undoBtn).removeAttr('disabled')
}
var gameOver = function() {
	return game.isOver
}
var isRedemption = function() {
	/* the redemption check as a boolean */
	return ($('#team1 .cups .active').length == 0) || ($('#team2 .cups .active').length == 0)
}
var checkRedemption = function() {
	/*
	 * calls the redemption dialogs
	 */
	console.debug('checking redemption')
	if ($('#team1 .cups .active').length == 0)
		redemption(1)
	if ($('#team2 .cups .active').length == 0)
		redemption(2)
}
var refreshCups = function() {
	/*
	 * refreshes the active status of cups on the screen using database info.
	 */
	console.debug('refreshing cups')
	for (var cupIdx = 1; cupIdx <= 6; cupIdx++) {
		game.team1.cups[cupIdx] ? deactivateCup(1, cupIdx) : activateCup(1, cupIdx)
		game.team2.cups[cupIdx] ? deactivateCup(2, cupIdx) : activateCup(2, cupIdx)
	}
}
/*
 *
 * Recording events and POST request
 *
 *
 */
var undoMove = function() {
	/* undoes the most recent event */
	postEvent('undo')
	documentRefresh()
}
var getGameStatus = function() {
	/*
	 * gets the database's current view of the game and updates the front end accordingly
	 */
	console.debug('getting game status from JSON')
	$.ajax({
		url : '../info/',
		async : false,
		dataType : 'json',
		success : function(data) {
			game['isOver'] = data.is_over
			game['team1'][1] = data.team1.user1
			game['team1'][2] = data.team1.user2
			game['team2'][1] = data.team2.user1
			game['team2'][2] = data.team2.user2

			for (var cupIdx = 1; cupIdx <= 6; cupIdx++) {
				game['team1']['cups'][cupIdx] = data.team1['cup' + cupIdx]
				game['team2']['cups'][cupIdx] = data.team2['cup' + cupIdx]
			}
		},
		error : function() {
			console.error('could not get JSON')
		}
	});
}
var postEvent = function(eventType, team, player, cup, cup2) {
	/*
	 * posts an event to this page
	 */
	console.debug('postEvent invoked')
	myData = {
		'eventType' : eventType,
		'team' : team,
		'player' : player
	}
	if (cup)
		myData['cup'] = cup
	if (cup2)
		myData['cup2'] = cup2

	console.debug('sending to post:', myData)
	$.ajax({
		type : 'POST',
		async : false,
		data : myData
	})
}
var recordEvent = function(type, team, player, cup) {
	console.debug('recording event')
	postEvent(type, team, player, cup, false)
	checkRedemption()
}
var recordBounce = function(team, player, cup1, cup2) {
	console.debug('recording bounce')
	postEvent('bounce', team, player, cup1, cup2)
	checkRedemption()
}
/*
 * Dialogs and such
 *
 */
var blamePlayer = function(team, blameFunction, closeOption) {
	/*
	* brings up a dialog box for the purpose of selecting the user who performed the last move.
	*  params:
	*   team: integer or string "teamX"
	* 		the team whose player is being questioned
	*   blameFunction: function(int player)
	* 		this function is invoked, which continues the blame process with a player to blame
	*/
	// if closeOption is defined as true OR undefined, can close. else false.
	closeOption = (closeOption || typeof closeOption == 'undefined')
	console.debug('called blame player')
	$('<div>').simpledialog2({
		mode : 'button',
		headerText : 'Who sunk that?',
		headerClose : closeOption,
		buttons : {
			'Player 1' : {
				id : 'button-player-1',
				click : function() {
					blameFunction(1)
				}
			},
			'Player 2' : {
				id : 'button-player-2',
				click : function() {
					blameFunction(2)
				}
			}
		},
		forceInput : false,
		showModal : true
	})
	/* edits this current simpledialog to show the current player names in the buttons */
	if ( typeof team == 'number')
		team = 'team' + team
	team = team == 'team1' ? 'team2' : 'team1'
	$("#button-player-1 .ui-btn-text").html(game[team][1])
	$("#button-player-2 .ui-btn-text").html(game[team][2])
}
/*
 * General cup interaction events
 *
 *
 */
var cupSunk = function(team, cup) {
	/*
	 * what happens when a cup is sunk
	 */
	console.debug('cup', cup, 'on team', team, 'was sunk')
	blamePlayer(team, function(player) {
		console.debug('Player', player, 'sunk the cup')
		deactivateCup(team, cup)
		recordEvent('regular', team, player, cup)
	})
}
var partyFoul = function(team, cup) {
	/*
	 * what happens when a party foul occurs
	 */
	console.debug('team', team, 'cup', cup, 'was a party foul')
	otherTeam = team == 'team1' ? 'team2' : 'team1'
	blamePlayer(otherTeam, function(player) {
		console.debug('Player', player, 'got a party foul')
		deactivateCup(team, cup)
		recordEvent('party_foul', otherTeam, player, cup)
	})
}
var trickShot = function(team, cup) {
	/*
	 * what happens when a trick shot occurs
	 */
	console.debug('team', team, 'cup', cup, 'was a trick shot')
	blamePlayer(team, function(player) {
		console.debug('Player', player, 'got a trick shot')
		deactivateCup(team, cup)
		recordEvent('trick', team, player, cup)
	})
}
var bounceShot = function(team, cup) {
	/*
	 * what happens when a bounce shot occurs
	 */
	console.debug('team', team, 'cup', cup, 'was a bounce shot')
	deactivateCup(team, cup)

	var selectBounceCup = function(team, cup, player) {
		console.debug('... by player', player)
		// here we are getting the HTML of the appropriate set of cups
		thatHtml = $('#' + team + ' .cups').html()
		// outHtml will contain thatHtml after appropriate modifications
		outHtml = ''
		i = 1
		$(thatHtml).filter('span').each(function() {
			// add class bcup, add attribute rel=close to close the dialog window on click
			$(this).addClass('bcup').attr('rel', 'close')
			// append this element to outHtml
			outHtml += $(this).prop('outerHTML')
			if (i == 1 || i == 3)
				outHtml += "<br/>"
			i += 1
		})
		var rotateClass = 'rotate-' + (team == 'team1' ? 'clockwise' : 'counterclockwise')

		$('<div>').simpledialog2({
			mode : 'blank',
			headerText : 'Second cup removed?',
			headerClose : false,
			blankContent : '<div class="cups ' + rotateClass + '">' + outHtml + '</div>'
		})

		$(document).delegate('.bcup.active', 'click', function() {
			/*
			 * delegate for the bounce shot bonus cup dialog
			 */
			var classes = this.className.split(' ')
			var team = classes[1]
			var cup2 = classes[2]
			console.debug('... and the bonus cup is', cup2)
			deactivateCup(team, cup2)
			recordBounce(team, player, cup, cup2)
			// DESTROYS THIS DELEGATE!! SUPER IMPORTANT :)
			$(document).undelegate('.bcup.active', 'click')
		})
	}
	if (!isRedemption()) {
		blamePlayer(team, function(player) {
			selectBounceCup(team, cup, player)
		})
	} else {
		blamePlayer(team, function(player) {
			recordEvent('bounce', team, player, cup)
		})
	}
}
/*
 * End condition events
 *
 *
 */
var redemption = function(winningTeam) {
	/*
	 * function invoked when all of one team's cups are gone
	 */
	var losingTeam = winningTeam == 1 ? 2 : 1
	$(this).simpledialog2({
		mode : 'button',
		headerText : 'Did team ' + losingTeam + ' redeem themselves?',
		buttons : {
			'Yes' : {
				click : function() {
					console.debug('they did redeem themselves')
					blamePlayer(losingTeam, function(player) {
						console.debug('player', player, 'got the redemption')
						undoMove()
						postEvent('redemption', 'team' + losingTeam, player, false, false)
					}, false)
				}
			},
			'No' : {
				click : function() {
					console.debug('did not redeem themselves')
					winningTeam = losingTeam == 1 ? 'team2' : 'team1'
					postEvent('win', winningTeam, 1, false, false)
					redirect('../summary/')
				}
			}
		},
		forceInput : false,
		showModal : true
	})
}
var forfeitTeam = function(winners) {
	/* invoked when a team forfeits */
	console.debug('team ' + winners + ' win because other team forfeited')
	postEvent('win', winners, 1, false, false)
	redirect('../summary/')
}
var deathCup = function(team) {
	/*
	 * invoked when a team gets a death cup
	 */
	console.debug('death cup by team ' + team)
	blamePlayer(team, function(player) {
		console.debug('Player', player, 'got the death cup')
		postEvent('death', team, player, false, false)
		postEvent('win', team, 1, false, false)
		redirect('../summary/')
	})
}
/*************************************************************************************************
 *************************************************************************************************
 **                                                                                             **
 **                              Global action event delegates                                  **
 **                                                                                             **
 *************************************************************************************************
 *************************************************************************************************/
var documentRefresh = function() {
	/* function called to refresh the state of the page */
	console.debug('refresh function')
	getGameStatus()
	if (!gameOver()) {
		refreshCups()
		refreshUndo()
	} else {
		$(document).undelegate()
		console.debug('bringing up menu')
		$('<div>').simpledialog2({
			mode : 'blank',
			headerText : 'This game has ended',
			blankContent : "<div style='padding: 10px'>" +
						   "<p style='text-align: center'>All actions are disabled.</br>" +
						   "<a href='../summary'>View game summary</a></p>" + 
						   "</div>"
		})
	}
}
var redirect = function(url) {
	/* just a consistent and clearly named way of redirecting to another url */
	self.location = url
}
$(document.body).ready(function() {
	/* function to refresh the document on load */
	console.debug('document loaded')
	documentRefresh()
})
$(document).delegate('.cup.active:not(".bcup")', 'click', function() {
	/*
	 * delegate for the main cup interface
	 */
	var classes = this.className.split(' ')
	var team = classes[1]
	var cup = classes[2]
	console.debug('team', team, 'cup', cup, 'was clicked')
	$(this).simpledialog2({
		mode : 'button',
		headerText : 'What happened?',
		headerClose : true,
		'buttons' : {
			'Cup Sunk' : {
				'click' : function() {
					cupSunk(team, cup)
				}
			},
			'Party Foul' : {
				'click' : function() {
					partyFoul(team, cup)
				}
			},
			'Bounce Shot' : {
				'click' : function() {
					bounceShot(team, cup)
				}
			},
			'Trick Shot' : {
				'click' : function() {
					trickShot(team, cup)
				}
			}
		},
		forceInput : false,
		showModal : true
	})
})
$(document).delegate('[name="rotate"]', 'click', function() {
	/* delegate for the rotate button */
	console.debug('clicked rotate')
	rotateCups()
})
$(document).delegate('[name="undo"]', 'click', function() {
	/* delegate for the undo button */
	console.debug('clicked undo')
	undoMove()
})
$(document).delegate('[name="abort"]', 'click', function() {
	/*
	 * delegate for the abort button
	 */
	console.debug('clicked abort')
	$('<div>').simpledialog2({
		mode : 'button',
		headerText : 'Are you sure?',
		headerClose : true,
		'buttons' : {
			'Yes' : {
				'click' : function() {
					console.debug('aborted game')
					redirect('profile/')
				}
			},
			'No' : {
				'click' : function() {
					console.debug('ignored abort')
				}
			}
		},
		forceInput : false,
		showModal : true
	})
})
$(document).delegate('[name="end"]', 'click', function() {
	/*
	 * delegate for the end game button
	 */
	console.debug('clicked end game')
	$('<div>').simpledialog2({
		mode : 'button',
		headerText : 'How did the game end?',
		headerClose : true,
		'buttons' : {
			'Forfeit' : {
				click : function() {
					console.debug('forfeit')
					$('<div>').simpledialog2({
						mode : 'button',
						headerText : 'Winning team?',
						headerClose : true,
						'buttons' : {
							'Team 1' : {
								click : function() {
									forfeitTeam(1)
								}
							},
							'Team 2' : {
								click : function() {
									forfeitTeam(2)
								}
							}
						},
						forceInput : false,
						showModal : true
					})
				}
			},
			'Death Cup' : {
				click : function() {
					console.debug('death cup')
					$('<div>').simpledialog2({
						mode : 'button',
						headerText : 'Winning team?',
						headerClose : true,
						'buttons' : {
							'Team 1' : {
								click : function() {
									deathCup('team1')
								}
							},
							'Team 2' : {
								click : function() {
									deathCup('team2')
								}
							}
						},
						forceInput : false,
						showModal : true
					})
				}
			}
		},
		forceInput : false,
		showModal : true
	})
})