from django.shortcuts import render, redirect
from .models import Worker
from django.conf import settings
import os
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Worker

# 1️⃣ Main worker list + adding workers
def worker_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')

        Worker.objects.create(
            name=name,
            phone=phone,
            email=email,
            gender=gender,
            role=role,
            address=address,
            photo=photo
        )

        return JsonResponse({'status': 'success', 'message': 'Worker added successfully!'})

    workers = Worker.objects.all()
    return render(request, 'workers/workers.html', {'workers': workers})


# Search workers via AJAX
def worker_search(request):
    query = request.GET.get('q', '').strip()

    workers = Worker.objects.all()
    if query:
        workers = workers.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query)
        )

    results = [{
        'id': w.id,
        'name': w.name,
        'phone': w.phone,
        'email': w.email,
        'role': w.role,
        'photo_url': w.photo.url if w.photo else '',
    } for w in workers]

    return JsonResponse({'results': results})



