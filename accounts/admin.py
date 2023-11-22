from django.contrib import admin
from .models import CustomUser, Contact


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ['username', 'first_name', 'last_name', 'email', 'confirm_email', 'date_joined', 'is_staff','is_active', 'is_superuser']


@admin.register(Contact)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'message', 'date']
