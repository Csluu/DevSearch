from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
# decorators for the signals 
from django.dispatch import receiver

# signals does stuff before or after something happens usually pre save, post save, pre delete and post delete
# NEED TO ADD TO THE LOCAL APPS.PY FILE!!!!! IN ORDER TO WORK 


# when a user is created it will create a profile for them based on the User model
# kwargs stands for key word arguments 
# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    print("its working")
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name)

# its deleting the user if the user profile is deleted as it automatically deletes the other way around
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    
# what the decorators are doing
post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)