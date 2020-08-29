from django import forms
from django.contrib.auth import get_user_model
from .models import MyProfile
from django.forms import ModelForm

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())


    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Are you sure you are registered with us?")
        return username


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password1 = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password", max_length=50, widget=forms.PasswordInput())

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password Do Not Matched!!!")
        else:
            return password2



