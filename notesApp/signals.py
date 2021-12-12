from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Note)
def createUpload(sender, instance, created, **kwargs):
    if created:
        Upload.objects.create(note=instance)

@receiver(post_save, sender=Note)
def saveUpload(sender, instance, **kwargs):
    instance.upload.save()