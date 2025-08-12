from django.shortcuts import render, redirect
from .models import Worker
from django.conf import settings
import os
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Worker
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


# 1️⃣ Main worker list + adding workers
def worker_list(request):
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')

   
        if worker_id:  # Update existing worker
            worker = get_object_or_404(Worker, id=worker_id)
            worker.name = name
            worker.phone = phone
            worker.email = email
            worker.gender = gender
            worker.role = role
            worker.address = address
            if photo:
                worker.photo = photo
            worker.save()
            return JsonResponse({'success': True, 'message': 'Worker updated successfully!'})

        else:  # Create new worker
            Worker.objects.create(
                name=name,
                phone=phone,
                email=email,
                gender=gender,
                role=role,
                address=address,
                photo=photo
            )
            return JsonResponse({'success': True, 'message': 'Worker added successfully!'})

    # Pagination setup
    workers = Worker.objects.all().order_by('-id')
    paginator = Paginator(workers, 10)  # 10 workers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_workers = workers.count()
    active_workers = workers.filter(is_active=True).count()
    inactive_workers = workers.filter(is_active=False).count()

    return render(request, 'workers/workers.html', {
        'workers': page_obj,
        'paginator': paginator,
        'page_obj': page_obj,
        'total_workers': total_workers,
        'active_workers': active_workers,
        'inactive_workers': inactive_workers,
    })


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
        'registered_on': w.registered_on.strftime("%Y-%m-%d") if w.registered_on else ''
    } for w in workers]

    return JsonResponse({'results': results})


# Get single worker details for editing
def get_worker(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    data = {
        'id': worker.id,
        'name': worker.name,
        'phone': worker.phone,
        'email': worker.email,
        'gender': worker.gender,
        'role': worker.role,
        'address': worker.address,
    }
    return JsonResponse(data)

@require_POST
def worker_delete(request, pk):
    try:
        worker = Worker.objects.get(pk=pk)
        worker.delete()
        return JsonResponse({'success': True, 'message': 'Worker deleted successfully!'})
    except Worker.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Worker not found.'}, status=404)



