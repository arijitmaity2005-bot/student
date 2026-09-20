from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, EmailOTP

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    fieldsets = UserAdmin.fieldsets + (
        ('Verification', {'fields': ('is_verified',)}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('is_verified', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer Profile Admin"""
    list_display = ('user_email', 'phone', 'created_at')
    search_fields = ('user__email', 'phone')
    list_filter = ('created_at',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    """Email OTP Admin"""
    list_display = ('email', 'otp', 'is_used', 'created_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('email', 'otp')
    readonly_fields = ('created_at',)

