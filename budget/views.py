from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date, timedelta
from .models import LedgerEntry, Category

@login_required
def budget_dashboard(request):
    user = request.user
    entries = LedgerEntry.objects.filter(user=user)
    categories = Category.objects.all()
    
    total_income = entries.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = entries.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    current_balance = total_income - total_expense
    
    semester_end = date(2026, 12, 20)
    days_remaining = (semester_end - date.today()).days
    days_remaining = max(0, days_remaining)
    
    two_weeks_ago = date.today() - timedelta(days=14)
    recent_non_essential = entries.filter(
        type='EXPENSE',
        category__is_essential=False,
        date__gte=two_weeks_ago
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    daily_velocity = recent_non_essential / 14
    
    if daily_velocity > 0:
        runway_days = int(current_balance / daily_velocity)
    else:
        runway_days = days_remaining

    noodle_alert = runway_days < days_remaining and current_balance > 0

    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        entry_type = request.POST.get('type')
        category_id = request.POST.get('category')
        
        cat = Category.objects.get(id=category_id) if category_id else None
        LedgerEntry.objects.create(user=user, title=title, amount=amount, type=entry_type, category=cat)
        return redirect('budget:budget')

    context = {
        'entries': entries[:10],
        'categories': categories,
        'current_balance': current_balance,
        'runway_days': runway_days,
        'days_remaining': days_remaining,
        'noodle_alert': noodle_alert,
    }
    return render(request, 'budget/dashboard.html', context)