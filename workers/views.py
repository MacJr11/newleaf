from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
import os
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from managementSystem.models import TaskAssignment
from django.utils.dateparse import parse_date
from django.db.models import Sum
from decimal import Decimal


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

def worker_profile(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)

    # All task assignments for this worker
    task_assignments = worker.taskassignment_set.select_related("order_item__po").prefetch_related("workers")

    total_tasks = task_assignments.count()
    completed_task = task_assignments.filter(order_item__status="Completed")
    completed_tasks = task_assignments.filter(order_item__status="Completed").count()

    # Calculate earnings
    total_earnings = 0
    for task in completed_task:
        if task.is_group_task:
            worker_share = (task.price_per_task * task.order_item.quantity) / task.workers.count() if task.workers.count() > 0 else 0
        else:
            worker_share = task.price_per_task
        total_earnings += worker_share
    
    total_paid = worker.payments.aggregate(s=Sum("amount"))["s"] or Decimal("0.00")
    payments = worker.payments.order_by("-payment_date", "-id")

    return render(request, "workers/worker_profile.html", {
        "worker": worker,
        "task_assignments": task_assignments,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "total_earnings": total_earnings,
        "total_paid": total_paid,
        "balance": (total_earnings - total_paid).quantize(Decimal("0.01")),
        'payments': payments
    })

@require_POST
def record_payment(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)

    amount = request.POST.get("amount")
    method = request.POST.get("method", "momo")
    reference = request.POST.get("reference", "")
    payment_date_str = request.POST.get("payment_date", "")

    # Basic validation
    try:
        amt = Decimal(amount)
        if amt <= 0:
            return JsonResponse({"success": False, "message": "Amount must be greater than 0."}, status=400)
    except Exception:
        return JsonResponse({"success": False, "message": "Invalid amount."}, status=400)

    # Optional: reject overpayment (comment this block if you allow overpay)
    # Recompute balance quickly
    
    tasks = worker.taskassignment_set.select_related("order_item__po").prefetch_related("workers")


    #tasks = TaskAssignment.objects.filter(workers=worker).select_related("order_item", "order_item__po")
    payable_tasks = tasks.filter(order_item__status="Completed")

    total_earnings = 0
    for task in payable_tasks:
        if task.is_group_task:
            worker_share = (task.price_per_task * task.order_item.quantity) / task.workers.count() if task.workers.count() > 0 else 0
        else:
            worker_share = task.price_per_task
        total_earnings += worker_share

    #total_earnings = sum((t.per_worker_share() for t in payable_tasks), Decimal("0.00"))
    
    total_paid = worker.payments.aggregate(s=Sum("amount"))["s"] or Decimal("0.00")
    balance = (total_earnings - total_paid)

    if amt > balance:
        return JsonResponse({"success": False, "message": f"Amount exceeds balance (GHS {balance:.2f})."}, status=400)

    # Parse date (optional)
    pay_date = parse_date(payment_date_str) if payment_date_str else None

    WorkerPayment.objects.create(
        worker=worker,
        amount=amt,
        method=method,
        reference=reference or None,
        payment_date=pay_date or timezone.now().date(),
    )

    return JsonResponse({"success": True, "message": "Payment recorded successfully."})
