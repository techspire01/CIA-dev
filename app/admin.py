from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Supplier, Announcement

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    # These are required for UserAdmin to work properly with CustomUser
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "business_description_display",
        "phone_number", 
        "formatted_address", 
        "created_at",
        'founder_name',
        'website_url',
        'category',
        'email',
        'contact_person_name'
    )
    
    def business_description_display(self, obj):
        """Display first 50 characters of business description"""
        if obj.business_description:
            return obj.business_description[:50] + "..." if len(obj.business_description) > 50 else obj.business_description
        return "-"
    business_description_display.short_description = "Business Description"
    
    def formatted_address(self, obj):
        """Format the address from individual fields"""
        address_parts = []
        if obj.door_number:
            address_parts.append(obj.door_number)
        if obj.street:
            address_parts.append(obj.street)
        if obj.area:
            address_parts.append(obj.area)
        if obj.city:
            address_parts.append(obj.city)
        if obj.state:
            address_parts.append(obj.state)
        if obj.pin_code:
            address_parts.append(obj.pin_code)
        
        return ", ".join(address_parts) if address_parts else "-"
    formatted_address.short_description = "Address"

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_critical', 'is_active')
    list_filter = ('is_critical', 'is_active', 'date')
    search_fields = ('title', 'content')
    ordering = ('-date',)
    date_hierarchy = 'date'

admin.site.register(CustomUser, CustomUserAdmin)
