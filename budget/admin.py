from django.contrib import admin
from .models import Category, LedgerEntry

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_essential')
    
    list_filter = ('is_essential',)
    
    search_fields = ('name',)

@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'type', 'category', 'date')
    
    list_filter = ('type', 'date', 'category', 'user')
    
    search_fields = ('title', 'user__username', 'category__name')
    
    readonly_fields = ('date',)