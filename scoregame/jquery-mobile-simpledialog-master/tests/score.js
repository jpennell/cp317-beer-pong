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
    $('<div></div>').simpledialog2({
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
    var selectBounceCup = function(team, cup, player) {
        console.log(team, 'player', player, 'had the bounce shot into', cup)
        
        var selteam = team == 'team1' ? 'team2' : 'team1'
        $("#"+selteam+" .cups").clone().appendTo('#select-bounce-cup')
        $('#select-bounce-cup .cup').each(function(){
          $(this).addClass('bcup')
        })
        
        $('#select-bounce-cup').simpledialog2();
        
        $('#bounce-cup').delegate('.bcup.active', 'click', function() {
            var cup = this.className.split(' ')[2]
            console.log('bounce shot off of', cup, 'and fuck yeah')
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

