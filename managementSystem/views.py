from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Sum, F, FloatField



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

    return render(request, 'orders/view_po.html', {
        'po': po,
        'items': items,
        'total_cost': total_cost,
        'workers': workers
    })