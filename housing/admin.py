from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'address', 
        'user', 
        'rent_price', 
        'status', 
        'campus_distance', 
        'transit_proximity', 
        'wifi_capability'
    )
    
    list_editable = ('status', 'rent_price')
    
    list_filter = ('status', 'user')
    
    search_fields = ('address', 'user__username')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'address', 'rent_price', 'status')
        }),
        ('Location & Tech Metrics', {
            'fields': ('campus_distance', 'transit_proximity', 'wifi_capability'),
            'description': 'Key metrics for evaluating student housing options.'
        }),
    )

    raw_id_fields = ('user',)