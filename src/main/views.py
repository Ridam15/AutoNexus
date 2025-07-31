from django.shortcuts import render,redirect, get_object_or_404
from importlib import reload
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from users.forms import LocationForm
from .models import listing as Listings,LikedListing
from .forms import ListingForm
from .filters import ListingFilter

def main_view(request):
    return render(request, 'views/main.html', {"name": "AutoMax", "message": "Your automated car management solution"})

@login_required
def home_view(request):
    listings=Listings.objects.all()
    listing_filter=ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(
        profile=request.user.profile).values_list('listing', flat=True)
    liked_listings_ids = list(user_liked_listings)
    context = {
        'listings': listings,
        'listing_filter': listing_filter,
        'liked_listings_ids': liked_listings_ids,
    }
    return render(request, 'views/home.html',context)

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.success(request, 'Listing created successfully!')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while processing your request. Please try again.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html',{'listing_form': listing_form,'location_form': location_form})

@login_required
def listing_view(request,id):
    try:
        listing= Listings.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request,'views/listing.html',{'listing': listing})
    except Exception as e:
        messages.error(request,f"Invalid UID {id} was provided for listing")
        return redirect('home')
    
@login_required
def edit_view(request,id):
    try:
        listing = Listings.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(request.POST, request.FILES, instance=listing)
            location_form = LocationForm(request.POST, instance=listing.location)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()   
                listing.refresh_from_db()
                messages.success(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                messages.error(request, f'An error occured while trying to access the edit page.')
                return reload()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
            context = {
                'listing_form': listing_form,
                'location_form': location_form,
            }
            return render(request, 'views/edit.html', context)
    except Exception as e:
        messages.error(request, f'An error occured while trying to access the edit page.')
        return redirect('home')
    
@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listings, id=id)

    liked_listing, created = LikedListing.objects.get_or_create(
        profile=request.user.profile, listing=listing)

    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user': created,
    })

@login_required
def inquire_listing_using_email(request, id):
    listing = get_object_or_404(Listings, id=id)
    try:
        email_subject = f'{request.user.username} is interested in {listing.model}'
        email_message = f'Hi {listing.seller.user.username}, {request.user.username} is interested in your {listing.model} listing on AutoMax'
        send_mail(email_subject, email_message, 'noreply@automax.com',
                  [listing.seller.user.email, ], fail_silently=True)
        messages.success(request, 'Inquiry email sent successfully!')
        return JsonResponse({
            "success": True,
        })  
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "info": e,
        })
 