from django.db import models
import uuid
from users.models import Profile,Location
from .consts import CARS_BRANDS,TRANSMISSION_OPTIONS
from .utils import user_listing_path
# Create your models here.

class listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True)
    brand = models.CharField(max_length=50, choices=CARS_BRANDS, default=CARS_BRANDS[0][0])
    model = models.CharField(max_length=64, default="")
    vin = models.CharField(max_length=17, default="")
    mileage = models.IntegerField(default=0)
    color = models.CharField(max_length=24, default="")
    description = models.TextField(default="")
    engine = models.CharField(max_length=24, default="")
    transmission = models.CharField(max_length=24, choices=TRANSMISSION_OPTIONS, default=TRANSMISSION_OPTIONS[0][0])
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, default=None)
    image = models.ImageField(upload_to=user_listing_path,blank=True,null=True)

    def __str__(self):
        return f"{self.seller.user.username}'s Listing - {self.model} "
    
class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'listing')

    def __str__(self):
        return f"{self.profile.user.username} liked {self.listing.model}"