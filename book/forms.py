from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'nickname',
            'profile_pic',
            'intro',
        ]
        Widgets = {
            'intro' : forms.Textarea,
        }