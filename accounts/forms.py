from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import *
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',  'password1', 'password2', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        for instance in User.objects.all():
            if instance.email == email:
                raise forms.ValidationError("Email Should Be Unique.")
     
        return email


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']