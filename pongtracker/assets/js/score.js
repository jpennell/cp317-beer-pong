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
 * global variables 
 * 
 */
game = {
	/* game information for dialog boxes */
	'team1' : {
		1 : "Team 1 Player 1",
		2 : "Team 1 Player 2"
	},
	'team2' : {
		1 : "Team 2 Player 1",
		2 : "Team 2 Player 2"
	}
}
/* array for storing most recent moves */
lastMoves = new Array()
/*
 * 
 * functions
 * 
 */
var editDialogText = function(team) {
	/* edits the current simpledialog to show the current player names in the buttons */
	$("#button-player-1 .ui-btn-text").html(game[team][1])
	$("#button-player-2 .ui-btn-text").html(game[team][2])
}
var canUndo = function() {
	/* checks whether there are moves to undo */
	return lastMoves.length > 0
}
var updateUndoButton = function() {
	/* updates the disabled status of the undo button */
	var undoBox = '[name="undo"]'
	canUndo() ? $(undoBox).removeAttr('disabled') : $(undoBox).attr('disabled', 'true')
}
var undoMove = function() {
	/* undoes the most recent event */
	if (!canUndo()) {
		console.error('nothing to undo!')
		return undefined
	}
	lastMove = lastMoves.pop()
	// construct css selector eg: .team1.cup1
	var sel = '.' + lastMove.team + '.' + lastMove.cup
	$(sel).addClass('active')
	if ( typeof lastMove.cup2 !== 'undefined') {
		var sel = '.' + lastMove.team + '.' + lastMove.cup2
		$(sel).addClass('active')
	}
}
var deactivateCup = function(team, cup) {
	/* makes a cup deactive (by removing CSS class 'active) */
	var selector = '.' + team + '.' + cup
	$(selector).removeClass('active')
}
/*
 * Recording events and POST request
 *
 *
 */
var postEvent = function(eventType, team, player, cup, cup2) {
	/*
	 * posts an event to this page
	 */
	myData = {
		'eventType' : eventType,
		'team' : team,
		'player' : player,
		'cup' : cup
	}
	if (cup2)
		myData['cup2'] = cup2

	console.log(eventType, team, player, cup, cup2)
	$.ajax({
		type : 'POST',
		data : myData
	})
}
var recordEvent = function(type, team, player, cup) {
	lastMoves.push({
		team : team,
		cup : cup
	})
	postEvent(type, team, player, cup, false)
}
var recordBounce = function(team, player, cup1, cup2) {
	lastMoves.push({
		team : team,
		cup : cup1,
		cup2 : cup2
	})
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
	 * 	 blameFunction: the function to invoke which continues the process
	 * 		blameFunction must take exactly one parameter, player
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
			"Player 2" : {
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
	editDialogText(team)
}
var cupSunk = function(team, cup) {
	/*
	 * what happens when a cup is sunk
	 */
	console.debug('cup', cup, 'on team', team, 'was sunk')
	var blameCupSunk = function(player) {
		console.debug('Player', player, 'sunk the cup')
		deactivateCup(team, cup)
		recordEvent('regular', team, player, cup)
	}
	blamePlayer(team, blameCupSunk)
}
var partyFoul = function(team, cup) {
	/*
	 * what happens when a party foul occurs
	 */
	console.debug('team', team, 'cup', cup, 'was a party foul')
	var blamePartyFoul = function(player) {
		console.debug('Player', player, 'got a party foul')
		deactivateCup(team, cup)
		recordEvent('party_foul', team, player, cup)
	}
	blamePlayer(team, blamePartyFoul)
}
var trickShot = function(team, cup) {
	/*
	 * what happens when a trick shot occurs
	 */
	console.debug('team', team, 'cup', cup, 'was a trick shot')
	var blameTrickShot = function(player) {
		console.debug('Player', player, 'got a trick shot')
		deactivateCup(team, cup)
		recordEvent('trick', team, player, cup)
	}
	blamePlayer(team, blameTrickShot)
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
			safeNuke : false,
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
		})
	}
	var selectBounceCupWrap = function(player) {
		selectBounceCup(team, cup, player)
	}
	blamePlayer(team, selectBounceCupWrap)
}
var rotateCups = function() {
	var t1 = '#team1 .cups'
	var t2 = '#team2 .cups'
	//var transforms = ['transform', '-webkit-transform', '-moz-transform']
	var transform = '-webkit-transform'
	$(t1).css(transform, $(t1).css(transform) == 'none' ? 'rotate( 90deg)' : '')
	$(t2).css(transform, $(t2).css(transform) == 'none' ? 'rotate(-90deg)' : '')
}
/*
* Global action event delegates
*
*/
// delegate for the main cup interface
$(document).delegate('.cup.active:not(".bcup")', 'click', function() {
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
})
// delegate for the end game button
$(document).delegate('[name="end"]', 'click', function() {
	console.debug('clicked end game')
})

