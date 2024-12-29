# Register your models here.

from django.contrib import admin
from userauths.models import User

class UserAdmin(admin.ModelAdmin):
    # Define list display fields for the admin interface
    list_display = ('username', 'email', 'gender', 'is_active', 'date_joined')
    # Add filters to the admin interface
    list_filter = ('is_active', 'is_staff')
    # Enable search functionality
    search_fields = ('username', 'email')

# Register the User model with the custom UserAdmin class
admin.site.register(User, UserAdmin)