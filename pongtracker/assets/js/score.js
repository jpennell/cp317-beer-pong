/*
 * score.js
 *
 * George Lifchits
 * July 2013
 *
 * JavaScript code which implements the Score Game aspect of the Pong Tracker project
 */

/*
 *
 * functions
 *
 */
game = {
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
	}
}
var refreshCups = function() {
	console.debug('refreshing cups')
	getGameStatus()
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
	console.debug('getting game status from JSON')
	$.ajax({
		url : '../info/',
		async: false,
		dataType : 'json',
		success : function(data) {
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
	console.debug('posting', eventType, team, player, cup, cup2)
	myData = {
		'eventType' : eventType,
		'team' : team,
		'player' : player
	}
	if (cup)
		myData['cup'] = cup
	if (cup2)
		myData['cup2'] = cup2

	console.log(eventType, team, player, cup, cup2)
	$.ajax({
		type : 'POST',
		async: false,
		data : myData
	})
}
var recordEvent = function(type, team, player, cup) {
	console.debug('recording event')
	postEvent(type, team, player, cup, false)
}
var recordBounce = function(team, player, cup1, cup2) {
	console.debug('recording bounce')
	postEvent('bounce', team, player, cup1, cup2)
}
/*
 * Dialogs and such
 *
 */
var blamePlayer = function(team, blameFunction) {
	/*
	 * brings up a dialog box for selecting the user who performed the last move
	 *  params:
	 *   team: integer or string "teamX"
	 * 		the team whose player is being questioned
	 * 	 blameFunction: function(int player)
	 * 		this function is invoked, which continues the blame process with a player to blame
	 */
	$(this).simpledialog2({
		mode : 'button',
		headerText : 'Who sunk that?',
		headerClose : true,
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
		showModal : true,
		clickEvent : 'vclick'
	})
	/* edits this current simpledialog to show the current player names in the buttons */
	if ( typeof team == 'number')
		team = 'team' + team
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
	blamePlayer(team, function(player) {
		console.debug('Player', player, 'got a party foul')
		deactivateCup(team, cup)
		recordEvent('party_foul', team, player, cup)
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
		// close all dialogs for good measure
		//$.mobile.sdCurrentDialog.close()
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

		$('<div>').simpledialog2({
			mode : 'blank',
			headerText : 'Second cup removed?',
			headerClose : false,
			blankContent : '<div class="cups">' + outHtml + '</div>'
		})

		// delegate for the bounce shot bonus cup dialog
		$(document).delegate('.bcup.active', 'click', function() {
			var classes = this.className.split(' ')
			var team = classes[1]
			var cup2 = classes[2]
			console.debug('... and the bonus cup is', cup2)
			deactivateCup(team, cup2)
			recordBounce(team, player, cup, cup2)
			$(document).undelegate('.bcup.active', 'click')
		})
	}
	blamePlayer(team, function(player) {
		selectBounceCup(team, cup, player)
	})
}
/*
 * End condition events
 *
 *
 */
var redemption = function(losingTeam) {
	$(this).simpledialog2({
		mode : 'button',
		headerText : 'Did team ' + losingTeam + ' redeem themselves?',
		buttons : {
			'Yes' : {
				click : function() {
					var blameRedemption = function(player) {
						console.debug('player', player, 'got the redemption')
						postEvent('redemption', 'team' + losingTeam, player, false, false)
						undoMove()
					}
					blamePlayer(losingTeam, blameRedemption)
				}
			},
			'No' : {
				click : function() {
					winningTeam = losingTeam == 1 ? 'team2' : 'team1'
					postEvent('win', winningTeam, 1, false, false)
				}
			}
		},
		forceInput : false,
		showModal : true,
		clickEvent : 'vclick'
	})
}
var isOnRedemption = function() {
	console.debug('checking if on redemption')
	team1cups = $('#team1 .cups .active')
	team2cups = $('#team2 .cups .active')
	if (team1cups.length == 0)
		redemption(1)
	if (team2cups.length == 0)
		redemption(2)
}
var forfeitTeam = function(winners) {
	console.log('team ' + winners + ' win because other team forfeited')
	// var postEvent = function(eventType, team, player, cup, cup2)
	postEvent('win', winners, 1, false, false)
}
var deathCup = function(team) {
	console.log('death cup by team ' + team)
	blamePlayer(team, function(player) {
		console.debug('Player', player, 'got the death cup')
		postEvent('death', team, player, false, false)
		postEvent('win', team, 1, false, false)
	})
}
/*
 * Other functions
 *
 *
 */
var rotateCups = function() {
	var t1 = '#team1 .cups'
	var t2 = '#team2 .cups'
	//var transforms = ['transform', '-webkit-transform', '-moz-transform']
	var transform = '-webkit-transform'
	$(t1).css(transform, $(t1).css(transform) == 'none' ? 'rotate( 90deg)' : '')
	$(t2).css(transform, $(t2).css(transform) == 'none' ? 'rotate(-90deg)' : '')
}
/**************************************************************************************************
 **************************************************************************************************
 **																								 **
 **									Global action event delegates								 **
 **																								 **
 **************************************************************************************************
 **************************************************************************************************/
var documentRefresh = function() {
	console.log('refresh function was invoked by delegate')
	refreshCups()
	var undoBtn = '[name="undo"]'
	if ($('cups span.active').length == 12)
		$(undoBtn).attr('disabled', 'true')
	else
		$(undoBtn).removeAttr('disabled')
}
// any click will refresh the document (temporary hack solution)
// $(document).delegate('html', 'click', documentRefresh)
$(document.body).ready(function() {
	/* refresh the document on load */
	console.log('document loaded')
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
		showModal : true,
		clickEvent : 'vclick'
	})
})
// delegate for the rotate button
$(document).delegate('[name="rotate"]', 'click', function() {
	console.debug('clicked rotate')
	rotateCups()
})
// delegate for the undo button
$(document).delegate('[name="undo"]', 'click', function() {
	console.debug('clicked undo')
	undoMove()
})
// delegate for the abort button
$(document).delegate('[name="abort"]', 'click', function() {
	console.debug('clicked abort')
	$('<div>').simpledialog2({
		mode : 'button',
		headerText : 'Are you sure?',
		headerClose : true,
		'buttons' : {
			'Yes' : {
				'click' : function() {
					console.debug('aborted game')
					self.location = '/profile/'
				}
			},
			'No' : {
				'click' : function() {
					console.debug('')
					return undefined
				}
			}
		},
		forceInput : false,
		showModal : true,
		clickEvent : 'vclick'
	})
})
// delegate for the end game button
$(document).delegate('[name="end"]', 'click', function() {
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
						showModal : true,
						clickEvent : 'vclick'
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
						showModal : true,
						clickEvent : 'vclick'
					})
				}
			}
		},
		forceInput : false,
		showModal : true,
		clickEvent : 'vclick'
	})
})

