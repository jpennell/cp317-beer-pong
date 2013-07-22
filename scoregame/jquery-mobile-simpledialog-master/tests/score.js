var deactivateCup = function(team, cup) {
	// construct css selector eg: .team1.cup1
	var sel = '.' + team + '.' + cup
	// remove "active" class for this cup
	$(sel).removeClass('active')
}
var cupSunk = function(team, cup) {
	console.log('cup', cup, 'on team', team, 'was sunk')
	deactivateCup(team, cup)
}
var partyFoul = function(team, cup) {
	console.log('team', team, 'cup', cup, 'was a party foul')
	var whoPartyFoul = function(player) {
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
					whoPartyFoul(1)
				}
			},
			'Player 2' : {
				'click' : function() {
					whoPartyFoul(2)
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
	var selectBounceCup = function(team, cup, player) {
		$(this).simpledialog2({
			mode : 'blank',
			headerText : 'Into which?',
			headerClose : true,
			blankContent : "<div class='cups' id='bounce'>" + "<style>#bounce{display: block; width: 200px; height: 200px;}</style>" + "<h1>Hello</h1>" + "</div>"
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

$(document).delegate('.cup.active', 'click', function() {
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
});

