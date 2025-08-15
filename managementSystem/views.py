from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Sum, F, FloatField
from django.db.models import Count
from django.contrib import messages


def register_client(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_email = request.POST.get('contact_email')
        phone = request.POST.get('phone')

        if client_id:
            client = get_object_or_404(Client, id=client_id)
            client.name = name
            client.phone = phone
            client.address = address
            client.email = contact_email
            client.save()
            return JsonResponse({'success': True, 'message': 'Worker updated successfully!'})
        else:
        # Basic validation example
            if name and contact_email:
                Client.objects.create(
                    name=name,
                    address=address,
                    contact_email=contact_email,
                    phone=phone,
                )
                return JsonResponse({'success': True, 'message': 'Worker added successfully!'})
            else:
                error = "Name and Email are required."
                return JsonResponse({'success': True, 'message': error})
    
    clients = Client.objects.all().order_by('-id')
    paginator = Paginator(clients, 10)  # 10 workers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'register_client.html', {
        'clients': page_obj,
        'paginator': paginator,
        'page_obj': page_obj,
    })
    

def get_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    data = {
        'id': client.id,
        'name': client.name,
        'phone': client.phone,
        'email': client.contact_email,
        'address': client.address,
    }
    return JsonResponse(data)

@require_POST
def client_delete(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        client.delete()
        return JsonResponse({'success': True, 'message': 'Client deleted successfully!'})
    except Client.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Client not found.'}, status=404)
    
def orders(request):
    orders = PurchaseOrder.objects.all().order_by('-id')

    total_orders = orders.count()
    completed_orders = orders.filter(status="Completed").count()
    inprogress_orders = orders.filter(status="In Progress").count()
    pending_orders = orders.filter(status="Pending").count()
    return render(request, 'orders/orders.html',{
        'orders': orders,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'inprogress_orders': inprogress_orders,
    })
    

def create_order(request):
    if request.method == 'POST':
        try:
            po_number = request.POST.get('po_number')
            client_id = request.POST.get('client')
            date_val = request.POST.get('date')
            due_date = request.POST.get('due_date')
            status = request.POST.get('status', 'Pending')

            if not all([po_number, client_id, date_val, due_date]):
                return JsonResponse({'success': False, 'message': 'All fields are required.'})

            client = Client.objects.get(id=client_id)
            PurchaseOrder.objects.create(
                po_number=po_number,
                client=client,
                date=date_val,
                due_date=due_date,
                status=status
            )

            return JsonResponse({'success': True, 'message': 'Purchase Order added successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    # GET request → show form normally
    clients = Client.objects.all()
    return render(request, 'orders/add_po.html', {'clients': clients})

def add_order_item(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    if request.method == 'POST':
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')

        OrderItem.objects.create(
            po=po,
            description=description,
            quantity=quantity,
            unit_price=unit_price
        )

        return redirect(reverse('managementSystem:view_po', args=[po.id]))

    return render(request, 'orders/add_order_item.html', {'po': po})

def view_po(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    items = OrderItem.objects.filter(po=po)

    total_items = items.count()
    # Calculate total cost of PO
    total_cost = items.aggregate(
        total=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
    )['total'] or 0

    # Get workers linked to this PO through TaskAssignments
    task_assignments = TaskAssignment.objects.filter(order_item__po=po).prefetch_related('workers')
    workers = set()
    
    for task in task_assignments:
        for worker in task.workers.all():
            workers.add(worker)

    # total workers
    assignments = TaskAssignment.objects.filter(order_item__in=items).prefetch_related('workers')

    workers_set = set()
    for assignment in assignments:
        for worker in assignment.workers.all():
            workers_set.add(worker.id)
    
    total_workers = len(workers_set)

    # Prepare items with their assigned workers
    item_workers = []
    for item in items:
        workers = Worker.objects.filter(
            taskassignment__order_item=item
        ).distinct()
        item_workers.append({
            "item": item,
            "workers": workers
        })

    #total workers on item
    for item in items:
        item.worker_count = TaskAssignment.objects.filter(order_item=item).aggregate(
            total_workers=Count('workers', distinct=True)
        )['total_workers'] or 0

    return render(request, 'orders/view_po.html', {
        'po': po,
        'items': items,
        'total_cost': total_cost,
        'workers': workers,
        'total_items': total_items,
        'total_workers': total_workers,
        "item_workers": item_workers,
    })


def assign_workers(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    items = OrderItem.objects.filter(po=po)

    # Filter workers to only active ones who are not already assigned to the same item
    workers = Worker.objects.filter(is_active=True)

    if request.method == "POST":
        order_item_id = request.POST.get("order_item")
        selected_workers = request.POST.getlist("workers")
        deadline = request.POST.get("deadline")
        is_group_task = request.POST.get("is_group_task") == "on"
        price_per_task = request.POST.get("price_per_task")

        # Validate selection
        if not selected_workers:
            messages.error(request, "No workers selected.")
            return redirect("managementSystem:assign_workers", po_id=po.id)

        if not is_group_task and len(selected_workers) > 1:
            messages.error(request, "You must mark as group task when assigning more than one worker.")
            return redirect("managementSystem:assign_workers", po_id=po.id)

        # Prevent assigning a worker who is already assigned to this order item
        existing_workers = Worker.objects.filter(
            taskassignment__order_item_id=order_item_id
        ).values_list("id", flat=True)
        duplicate_ids = set(map(int, selected_workers)) & set(existing_workers)
        if duplicate_ids:
            messages.warning(request, "Some selected workers are already assigned to this task.")
            return redirect("managementSystem:assign_workers", po_id=po.id)

        # Create task assignment
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        task = TaskAssignment.objects.create(
            order_item=order_item,
            deadline=deadline,
            is_group_task=is_group_task,
            price_per_task=price_per_task
        )
        task.workers.set(selected_workers)

        messages.success(request, "Workers assigned successfully!")
        return redirect("managementSystem:view_po", po_id=po.id)

    return render(request, "orders/assign_workers.html", {
        "po": po,
        "items": items,
        "workers": workers
    })
