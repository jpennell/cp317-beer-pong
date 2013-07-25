from django import forms

CHOICES = [('confirm','confirm'),('deny','deny')]

class ConfirmGameForm(forms.Form):
    confirm = forms.ChoiceField(choices = CHOICES, widget = forms.RadioSelect())