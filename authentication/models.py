from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)