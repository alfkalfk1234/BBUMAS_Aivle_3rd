from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'pswd1'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'name', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'id': 'id'}),
            'name': forms.TextInput(attrs={'id': 'name'}),
            'email': forms.EmailInput(attrs={'id': 'email'}),
            'phone': forms.TextInput(attrs={'id': 'phone'}),
        }
