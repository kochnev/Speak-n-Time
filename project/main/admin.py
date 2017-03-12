from django.contrib import admin
from .models import UserProfile, Language, UserLanguage

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Language)
admin.site.register(UserLanguage) 
