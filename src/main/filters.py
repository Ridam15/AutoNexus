import django_filters

from .models import listing

class ListingFilter(django_filters.FilterSet):
    class Meta:
        model = listing
        fields = {
            'brand': ['exact'],
            'model': ['exact', 'icontains'],
            'color': ['exact'],
            'engine': ['exact'],
            'transmission': ['exact'],
            'mileage': ['lt', 'gt'],
        }
        