from django import forms

class CreateGameForm(forms.Form):
    
    username2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label="Player 2",
        max_length=20)
    
    username3 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label="Player 3",
        max_length=20)
    
    username4 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label="Player 4",
        max_length=20)
    
    email2 = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        label="Email",
        max_length=40,
        required = False)
    
    email3 = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        label="Email",
        max_length=40,
        required = False)
    
    email4 = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        label="Email",
        max_length=40,
        required = False)
    
    err2 = ''
    err3 = ''
    err4 = ''