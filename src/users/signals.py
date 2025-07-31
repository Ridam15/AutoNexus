from django.contrib.auth.models import User
from .models import Profile,Location
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def create_profile_location(sender, instance, created, **kwargs):
    if created:
        location=Location.objects.create()
        instance.location = location
        instance.save()

@receiver(post_delete, sender=Profile)
def delete_profile_location(sender, instance, *args, **kwargs):
    if instance.location:
        instance.location.delete()