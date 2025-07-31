from django.contrib import admin
from .models import listing,LikedListing
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    readonly_fields =('id',)

class LikedListingAdmin(admin.ModelAdmin):
    readonly_fields =('id',)

admin.site.register(listing, ListingAdmin)
admin.site.register(LikedListing, LikedListingAdmin)
 