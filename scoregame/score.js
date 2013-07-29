/*
 * score.js
 *
 * George Lifchits
 * July 2013
 *
 * JavaScript code which implements the Score Game aspect of the Pong Tracker project
 */

lastMoves = new Array()

move = {
	team : '',
	cup : ''
}

var undoMove = function() {
	lastMove = lastMoves.pop()
	if (lastMove == undefined) {
		console.error('nothing to undo!')
		return undefined
	}
	// construct css selector eg: .team1.cup1
	var sel = '.' + lastMove.team + '.' + lastMove.cup
	$(sel).addClass('active')
}
var deactivateCup = function(team, cup) {
	// construct css selector eg: .team1.cup1
	var sel = '.' + team + '.' + cup
	$(sel).removeClass('active')
	lastMoves.push({
		team : team,
		cup : cup
	})
}
var cupSunk = function(team, cup) {
	console.debug('cup', cup, 'on team', team, 'was sunk')
	deactivateCup(team, cup)
}
var partyFoul = function(team, cup) {
	console.debug('team', team, 'cup', cup, 'was a party foul')
	var blamePartyFoul = function(player) {
		console.debug('Player', player, 'got a party foul')
		deactivateCup(team, cup)
	}
	$(this).simpledialog2({
		mode : 'button',
		headerText : 'Who?',
		headerClose : true,
		'buttons' : {
			'Player 1' : {
				'click' : function() {
					blamePartyFoul(1)
				}
			},
			'Player 2' : {
				'click' : function() {
					blamePartyFoul(2)
				}
			}
		},
		forceInput : false,
		showModal : true,
		clickEvent : 'vclick'
	})
}
var trickShot = function(team, cup) {
	console.debug('team', team, 'cup', cup, 'was a trick shot')
	deactivateCup(team, cup)
}
var bounceShot = function(team, cup) {
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
			headerText : 'Which cup?',
			safeNuke : false,
			headerClose : false,
			blankContent : '<div class="cups">' + outHtml + '</div>'
		})
	}

	$(this).simpledialog2({
		mode : 'button',
		headerText : 'Who?',
		headerClose : true,
		'buttons' : {
			'Player 1' : {
				'click' : function() {
					selectBounceCup(team, cup, 1)
				}
			},
			'Player 2' : {
				'click' : function() {
					selectBounceCup(team, cup, 2)
				}
			}
		},
		forceInput : false,
		showModal : true,
		clickEvent : 'vclick'
	})
}

var rotateCups = function() {
	var t1 = '#team1 .cups'
	var t2 = '#team2 .cups'
	if ($(t1).css('-webkit-transform') == 'none')
		$(t1).css('-webkit-transform','rotate(90deg)')
	else
		$(t1).css('-webkit-transform','')
		
	if ($(t2).css('-webkit-transform') == 'none')
		$(t2).css('-webkit-transform','rotate(-90deg)')
	else
		$(t2).css('-webkit-transform','')
}

/*
 * Action event delegates
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
		headerText : 'What Happened?',
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
// delegate for the bounce shot bonus cup dialog
$(document).delegate('.bcup.active', 'click', function() {
	var classes = this.className.split(' ')
	var team = classes[1]
	var cup = classes[2]
	console.debug('... and the bonus cup is', cup)
	deactivateCup(team, cup)
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

