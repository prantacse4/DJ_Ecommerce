from django import forms
from .models import *

class SearchForm(forms.Form):
    query = forms.CharField( max_length=50)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']