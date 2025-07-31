def user_listing_path(instance, filename): 
    return 'users/{0}/listing_images/{1}'.format(instance.seller.user.id, filename)