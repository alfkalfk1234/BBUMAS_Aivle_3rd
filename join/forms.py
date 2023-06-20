from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'name', 'email', 'phone']
