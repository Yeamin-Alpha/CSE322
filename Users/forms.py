# forms.py
from django import forms
from .models import ProfileImage
#Yeamin
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']
