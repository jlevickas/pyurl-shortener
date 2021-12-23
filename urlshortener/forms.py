from django import forms
from django.forms import TextInput


class URLForm(forms.Form):
    url = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Your URL', 'autocomplete': 'off', 'class': 'form-control', 'aria-describedby': 'button-addon1'}))
