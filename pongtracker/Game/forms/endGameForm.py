from django import forms

class EndGameForm(forms.Form):
    
    users = [None,None,None,None]
    ranks = [None,None,None,None]
    stats = [None,None,None,None,None,None]
    winner = None
   
    authErr = False