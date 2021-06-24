from django.contrib import admin
from .models import *
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'image_tag']
    list_filter  = ['user' ]

admin.site.register(UserProfile, UserProfileAdmin)