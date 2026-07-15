from django.contrib import admin
from django.utils.html import format_html
from .models import Household, SharedExpense, ExpenseSplit, Chore


class ExpenseSplitInline(admin.TabularInline):
    model = ExpenseSplit
    extra = 1  
    fields = ('user', 'amount_owed')


class ChoreInline(admin.TabularInline):
    model = Chore
    extra = 0
    fields = ('title', 'assigned_to', 'due_date', 'is_completed')



@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('name', 'invite_code', 'get_member_count')
    search_fields = ('name', 'invite_code')
    filter_horizontal = ('members',)
    inlines = [ChoreInline]

    @admin.display(description='Total Members')
    def get_member_count(self, obj):
        return obj.members.count()


@admin.register(SharedExpense)
class SharedExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'household', 'payer', 'total_amount', 'timestamp')
    list_filter = ('household', 'payer', 'timestamp')
    search_fields = ('title', 'household__name', 'payer__username')
    inlines = [ExpenseSplitInline]


@admin.register(ExpenseSplit)
class ExpenseSplitAdmin(admin.ModelAdmin):
    list_display = ('expense', 'user', 'amount_owed')
    list_filter = ('user', 'expense__household')
    search_fields = ('expense__title', 'user__username')


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'household', 'assigned_to', 'due_date', 'is_completed', 'karma_points', 'preview_proof_image')
    list_filter = ('is_completed', 'due_date', 'household', 'assigned_to')
    search_fields = ('title', 'household__name', 'assigned_to__username')
    list_editable = ('is_completed', 'assigned_to') 
    readonly_fields = ('preview_proof_image_large',)

    @admin.display(description='Proof Preview')
    def preview_proof_image(self, obj):
        """Displays a tiny thumbnail in the list view."""
        if obj.proof_image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px;" />', obj.proof_image.url)
        return "No proof"

    @admin.display(description='Chore Proof Image')
    def preview_proof_image_large(self, obj):
        """Displays a larger preview in the detail/edit view."""
        if obj.proof_image:
            return format_html('<img src="{}" style="max-width: 400px; max-height: 400px; border-radius: 8px;" />', obj.proof_image.url)
        return "No proof uploaded yet."