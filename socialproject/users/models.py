from django.db import models
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    bio = models.CharField(max_length=240, blank=True)
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="followers",
        blank=True,
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
    
