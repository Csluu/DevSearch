from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
# decorators for the signals 
from django.dispatch import receiver

# signals does stuff before or after something happens usually pre save, post save, pre delete and post delete
# using signals to modify User stuff when Profile gets update - so what we're not messing with user stuff directly 
# NEED TO ADD TO THE LOCAL APPS.PY FILE!!!!! IN ORDER TO WORK 


# when a user is created it will create a profile for them based on the User model
# kwargs stands for key word arguments 
# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        
def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    # making sure this doesn't loop back and forth between createProfile and updateProfile forever
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# its deleting the user if the user profile is deleted as it automatically deletes the other way around
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    
# what the decorators are doing
post_save.connect(createProfile, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)