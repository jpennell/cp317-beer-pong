/*
 * score.js
 *
 * George Lifchits
 * July 2013
 *
 * JavaScript code which implements the Score Game aspect of the Pong Tracker project
 */

var deactivateCup = function(team, cup) {
	// construct css selector eg: .team1.cup1
	var sel = '.' + team + '.' + cup
	$(sel).removeClass('active')
}
var cupSunk = function(team, cup) {
	console.log('cup', cup, 'on team', team, 'was sunk')
	deactivateCup(team, cup)
}
var partyFoul = function(team, cup) {
	console.log('team', team, 'cup', cup, 'was a party foul')
	var blamePartyFoul = function(player) {
		console.log('Player', player, 'got a party foul')
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
	console.log('team', team, 'cup', cup, 'was a trick shot')
	deactivateCup(team, cup)
}
var bounceShot = function(team, cup) {
	console.log('team', team, 'cup', cup, 'was a bounce shot')
	deactivateCup(team, cup)

	var selectBounceCup = function(team, cup, player) {
		console.log('... by player', player)
		// close all dialogs for good measure
		$.mobile.sdCurrentDialog.close()
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
// starting point of the program
$(document).delegate('.cup.active:not(".bcup")', 'click', function() {
	var classes = this.className.split(' ')
	var team = classes[1]
	var cup = classes[2]
	console.log('team', team, 'cup', cup, 'was clicked')
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

$(document).delegate('.bcup.active', 'click', function() {
	var classes = this.className.split(' ')
	var team = classes[1]
	var cup = classes[2]
	console.log('... and the bonus cup is', cup)
	deactivateCup(team, cup)
})

