from django import forms
from .models import Post, Photo

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_content', 'post_image']  # 'post_image'를 추가하세요.
        
        widgets = {
            'post_title': forms.TextInput(attrs={'id': 'post_title'}),
            'post_content': forms.TextInput(attrs={'id': 'post_content'}),
            'post_image': forms.FileInput(attrs={'id': 'post_image', 'onchange': "dropFile.handleFiles(this.files)", 'accept': "image/png, image/jpeg, image/gif"}),  # 이미지 입력 위젯을
        }

# class PhotoForm(forms.ModelForm):
#     class Meta:
#         model = Photo
#         fields = ['latitude', 'longitude', 'timestamp', 'detected_object', 'photo_path']
