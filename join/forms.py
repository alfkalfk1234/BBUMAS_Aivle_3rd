from django import forms
from .models import CustomUser

from django import forms
from django.core.validators import RegexValidator

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

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['phone'].validators.append(
            RegexValidator(
                regex=r'^010\d{8}$',
                message="전화번호는 '010'으로 시작하고 뒤에는 8자리 숫자가 와야합니다.",
                code='invalid_number'
            )
        )
        
        self.fields['username'].validators.append(
            RegexValidator(
                regex=r'^[a-zA-Z0-9]{5,}$',
                message="사용자 이름은 영어 알파벳과 숫자로 구성된 5자리 이상의 문자열이어야 합니다.",
                code='invalid_username'
            )
        )

