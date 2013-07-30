/*
 * score.js
 *
 * George Lifchits
 * July 2013
 *
 * JavaScript code which implements the Score Game aspect of the Pong Tracker project
 */

alert(user1 + ', ' + user2 + ', ' + user3 + ', ' + user4)

lastMoves = new Array()

move = {
	team : '',
	cup : '',
	bounce : undefined
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
	if (lastMove.bounce != undefined) {
		var sel = '.' + lastMove.bounce.team + '.' + lastMove.bounce.cup
		$(sel).addClass('active')
	}
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
var blamePlayer = function(blameFunction) {
	$(this).simpledialog2({
		mode : 'button',
		headerText : 'Who sunk that?',
		headerClose : true,
		buttons : {
			user1 : {
				click : function() {
					blameFunction(1)
				}
			},
			btn2 : {
				click : function() {
					blameFunction(2)
				}
			}
		},
		forceInput : false,
		showModal : true,
		clickEvent : 'vclick'
	})
}
var cupSunk = function(team, cup) {
	console.debug('cup', cup, 'on team', team, 'was sunk')
	var blameCupSunk = function(player) {
		console.debug('Player', player, 'sunk the cup')
		deactivateCup(team, cup)
	}
	blamePlayer(blameCupSunk)
}
var partyFoul = function(team, cup) {
	console.debug('team', team, 'cup', cup, 'was a party foul')
	var blamePartyFoul = function(player) {
		console.debug('Player', player, 'got a party foul')
		deactivateCup(team, cup)
	}
	blamePlayer(blamePartyFoul)
}
var trickShot = function(team, cup) {
	console.debug('team', team, 'cup', cup, 'was a trick shot')
	var blameTrickShot = function(player) {
		console.debug('Player', player, 'got a trick shot')
		deactivateCup(team, cup)
	}
	blamePlayer(blameTrickShot)
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
			headerText : 'Second cup removed?',
			safeNuke : false,
			headerClose : false,
			blankContent : '<div class="cups">' + outHtml + '</div>'
		})
	}
	var selectBounceCupWrap = function(player) {
		selectBounceCup(team, cup, player)
	}
	blamePlayer(selectBounceCupWrap)
}
var rotateCups = function() {
	var t1 = '#team1 .cups'
	var t2 = '#team2 .cups'
	if ($(t1).css('-webkit-transform') == 'none')
		$(t1).css('-webkit-transform', 'rotate(90deg)')
	else
		$(t1).css('-webkit-transform', '')

	if ($(t2).css('-webkit-transform') == 'none')
		$(t2).css('-webkit-transform', 'rotate(-90deg)')
	else
		$(t2).css('-webkit-transform', '')
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

