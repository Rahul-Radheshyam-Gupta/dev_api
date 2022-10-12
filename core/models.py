from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='profile', null=True)
    rank = models.CharField(max_length=3, default=5)
    otp = models.CharField(max_length=4, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name if self.first_name else self.user.username
