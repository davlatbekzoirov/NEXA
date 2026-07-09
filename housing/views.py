from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Property


@login_required
def crm_pipeline(request):
    properties = Property.objects.filter(user=request.user)
    
    if request.method == 'POST':
        address = request.POST.get('address')
        rent = request.POST.get('rent_price')
        distance = request.POST.get('campus_distance')
        transit = request.POST.get('transit_proximity')
        wifi = request.POST.get('wifi_capability')
        
        Property.objects.create(
            user=request.user, address=address, rent_price=rent,
            campus_distance=distance, transit_proximity=transit, wifi_capability=wifi
        )
        return redirect('housing:pipeline')

    context = {
        'found': properties.filter(status='FOUND'),
        'scheduled': properties.filter(status='SCHEDULED'),
        'applied': properties.filter(status='APPLIED'),
        'signed': properties.filter(status='SIGNED'),
    }
    return render(request, 'housing/pipeline.html', context)

@login_required
def update_status(request, pk, status):
    prop = get_object_or_404(Property, id=pk, user=request.user)
    prop.status = status
    prop.save()
    return redirect('housing:pipeline')