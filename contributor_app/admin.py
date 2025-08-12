from django.contrib import admin
from .models import UserProfile, DataEntry, CustomUser

admin.site.register(UserProfile)
admin.site.register(DataEntry)
admin.site.register(CustomUser)