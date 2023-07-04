from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'pswd1','placeholder': 'PassWord'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'name', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'id': 'id','placeholder': 'ID'}),
            'name': forms.TextInput(attrs={'id': 'name','placeholder': '예) 홍길동'}),
            'email': forms.EmailInput(attrs={'id': 'email','placeholder': '예) kt123@kt.com'}),
            'phone': forms.TextInput(attrs={'id': 'phone','placeholder': '예) 01012345678'}),
        }
