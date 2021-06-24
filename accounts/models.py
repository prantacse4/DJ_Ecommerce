from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=50)
    address = models.CharField(blank=True, null=True, max_length=50)
    city = models.CharField(blank=True, null=True, max_length=50)
    country = models.CharField(blank=True, null=True, max_length=50)
    image = models.ImageField(upload_to='user/', blank=True)
    def __str__(self):
        return self.user.username
    
    def user_name(self):
        return self.user.first_name+ ' '+self.user.last_name+'['+self.user.username+']'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    def imageurl(self):
        if self.image:
            return self.image.url
        else:
            return ""
