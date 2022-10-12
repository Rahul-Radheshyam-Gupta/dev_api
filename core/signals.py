from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import pre_save
from core.models import Profile
from django.contrib.auth.models import User

@receiver(pre_save, sender=Profile)
def my_callback(sender,instance, **kwargs):
    if instance._state.adding:
        print("Profile Created")
        try:
            print(instance.user)
        except:
            print("Failed to link a user")
        # user = User.objects.create_user(instance.username, instance.email, instance.password)
