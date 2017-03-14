from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Language, UserLanguage

# Register your models here.
#admin.site.register(UserProfile)
#admin.site.register(Language)
#admin.site.register(UserLanguage)
admin.site.unregister(User)

class UserProfileInstanceInline(admin.StackedInline):
    model = UserProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInstanceInline]

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name','code')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','website','gender','birthday')
    list_filter = ('gender', 'website')
    fieldsets = (
        (None, {
            'fields': ('user', 'website', 'birthday')
        }),
        ('Additional', {
            'fields': ('picture', 'gender')
        })
    )

@admin.register(UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'language', 'native')
