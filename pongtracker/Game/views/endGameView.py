

def viewGameSummaryRequest(request, game_id):
    
    username = request.session['username']
    
    # on POST
    if request.method == 'POST':
        
        
    
    else:
        return render(request, 'game_id/summary/')