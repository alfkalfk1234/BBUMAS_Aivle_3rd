from django import forms

class DamageForm(forms.Form):
    damages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

from django import forms
from .models import Detection

class DetectionForm(forms.ModelForm):
    checkedRows = forms.CharField(widget=forms.HiddenInput())  # Hidden field for the checked rows

    class Meta:
        model = Detection
        fields = ['latitude', 'longitude', 'detected_object', 'detected_time', 'detected_where', 'image_path', 'checkedRows','video_region']  # Include checked_rows in the fields

