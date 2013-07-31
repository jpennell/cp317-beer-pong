from django import forms

class EndGameForm(forms.Form):
    
    usernames = [None,None,None,None]
    ranks = [None,None,None,None]
    stats = [None,None,None,None,None]
   
    authErr = False