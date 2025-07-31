from django import forms
from django.contrib.auth.models import User
from .widgets import CustomPictureImageFieldWidget

from .models import Location,Profile

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
       

class ProfileForm(forms.ModelForm):
    photo=forms.ImageField(widget=CustomPictureImageFieldWidget)
    bio=forms.TextInput(attrs={'placeholder': 'Tell us about yourself'})

    class Meta:
        model = Profile
        fields = ['photo','phone_number', 'bio']


class LocationForm(forms.ModelForm):
    address_1 = forms.CharField(required=True)
    class Meta:
        model = Location
        fields = {'address_1', 'address_2', 'city', 'state', 'zip_code'}
        
