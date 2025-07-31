from django import forms
from .models import listing

class ListingForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = listing
        fields = {'brand', 'model', 'vin', 'mileage',
                  'color', 'description', 'engine', 'transmission', 'image'}