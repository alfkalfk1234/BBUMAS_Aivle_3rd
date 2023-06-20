from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'name', 'email', 'phone']
