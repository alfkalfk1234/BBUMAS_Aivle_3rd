from django import forms

class DamageForm(forms.Form):
    damages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
