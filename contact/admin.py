from django.contrib import admin
from .models import UserProfile, ContactSubscribe, Relationship


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'avatar', 'gender', 'created']


@admin.register(ContactSubscribe)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['email', 'date']

admin.site.register(Relationship)