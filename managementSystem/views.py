from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Sum, F, FloatField, ExpressionWrapper, DecimalField
from django.db.models import Count
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncWeek, TruncMonth, TruncYear, TruncDay
from django.utils.timezone import now
from datetime import date, timedelta, datetime
from django.http import HttpResponse
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
import io
import os


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
    inprogress_orders = orders.filter(status="In progress").count()
    pending_orders = orders.filter(status="Pending").count()
    return render(request, 'orders/orders.html',{
        'orders': orders,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'inprogress_orders': inprogress_orders,
    })

# Search PO via AJAX
def po_search(request):
    query = request.GET.get('q', '').strip()

    orders = PurchaseOrder.objects.all()
    if query:
        orders = orders.filter(
            Q(po_number__icontains=query) |
            Q(status__icontains=query) |
            Q(date__icontains=query) |
            Q(date__icontains=query)
        )

    results = [{
        'id': p.id,
        'po_number': p.po_number,
        'client': p.client.name,
        'date': p.date.strftime("%Y-%m-%d"),
        'due_date': p.due_date.strftime("%Y-%m-%d"),
        'status': p.status,
    } for p in orders]

    return JsonResponse({'results': results})
    

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

def edit_po(request, po_id):
    order = get_object_or_404(PurchaseOrder, id=po_id)
    clients = Client.objects.all()

    if request.method == "POST":
        order.po_number = request.POST.get("po_number")
        order.client_id = request.POST.get("client")
        order.date = request.POST.get("date")
        order.due_date = request.POST.get("due_date")
        order.status = request.POST.get("status")
        order.save()

        return JsonResponse({
            "success": True,
            "message": "Purchase order updated successfully!"
        })
    return render(request, 'orders/edit_po.html',{
        'order': order,
        'clients': clients,
        'po': order
    })

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

    # # total workers
    # assignments = TaskAssignment.objects.filter(order_item__in=items).prefetch_related('workers')

    # # workers_set = set()
    # # for assignment in assignments:
    # #     for worker in assignment.workers.all():
    # #         workers_set.add(worker.id)
    
    # # total_workers = len(workers_set)

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
        item.worker_count = TaskAssignment.objects.filter(order_item=item) \
            .annotate(num_workers=Count('workers')) \
            .aggregate(total_workers=Sum('num_workers'))['total_workers'] or 0
    
    grand_total_workers = sum(item.worker_count for item in items)

    return render(request, 'orders/view_po.html', {
        'po': po,
        'items': items,
        'total_cost': total_cost,
        'workers': workers,
        'total_items': total_items,
        'grand_total_workers': grand_total_workers,
        "item_workers": item_workers,
        "task_assignments": task_assignments

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
            messages.warning(request, "No workers selected.")
            return redirect("managementSystem:assign_workers", po_id=po.id)

        if not is_group_task and len(selected_workers) > 1:
            messages.warning(request, "You must mark as group task when assigning more than one worker.")

        # Prevent assigning a worker who is already assigned to this order item
        existing_workers = Worker.objects.filter(
            taskassignment__order_item_id=order_item_id
        ).values_list("id", flat=True)
        duplicate_ids = set(map(int, selected_workers)) & set(existing_workers)
        if duplicate_ids:
            messages.warning(request, "Some selected workers are already assigned to this task.")

        
        order_item = get_object_or_404(OrderItem, id=order_item_id)    
        existing_task = TaskAssignment.objects.filter(order_item=order_item).first()

        if existing_task:
            # Append new workers to existing task
            current_workers = set(existing_task.workers.values_list("id", flat=True))
            new_workers = set(map(int, selected_workers))
            all_workers = current_workers.union(new_workers)
            existing_task.workers.set(all_workers)

            # Automatically switch to group task if workers > 1
            if len(all_workers) > 1:
                existing_task.is_group_task = True

            # update other fields if needed
            existing_task.deadline = deadline
            existing_task.price_per_task = price_per_task
            existing_task.save()
            messages.success(request, "Workers assigned successfully!")
        else:
            # Create task assignment
            task = TaskAssignment.objects.create(
                order_item=order_item,
                deadline=deadline,
                is_group_task=is_group_task,
                price_per_task=price_per_task
            )
            task.workers.set(selected_workers)
            messages.success(request, "Workers assigned successfully!")

    return render(request, "orders/assign_workers.html", {
        "po": po,
        "items": items,
        "workers": workers
    })

def edit_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)

    if request.method == "POST":
        item.description = request.POST.get("description")
        item.quantity = request.POST.get("quantity")
        item.unit_price = request.POST.get("unit_price")
        item.save()

        return JsonResponse({"success": True, "message": "Item updated successfully!"})

    return render(request, "orders/edit_order_item.html", {
        "item": item,
    })

def delete_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    po_id = item.po.id
    item.delete()
    return JsonResponse({"success": True, "message": "Item deleted successfully!"})


def edit_task_assignment(request, task_id):
    task = get_object_or_404(TaskAssignment, id=task_id)
    workers = Worker.objects.filter(is_active=True)

    orderItem = get_object_or_404(OrderItem, id=task.order_item.id)

    if request.method == "POST":
        selected_workers = request.POST.getlist("workers")
        deadline = request.POST.get("deadline")
        is_group_task = request.POST.get("is_group_task") == "on"
        price_per_task = request.POST.get("price_per_task")
        status = request.POST.get("status")

        # Rules
        if len(selected_workers) == 1 and is_group_task:
            return JsonResponse({"success": False, "message": "Group task cannot be set with only one worker."})
        if len(selected_workers) > 1 and not is_group_task:
            return JsonResponse({"success": False, "message": "Multiple workers require group task selection."})

        task.deadline = deadline
        task.is_group_task = is_group_task
        task.price_per_task = price_per_task
        task.workers.set(selected_workers)
        task.save()

        orderItem.status = status
        orderItem.save()

        return JsonResponse({"success": True, "message": "Task assignment updated successfully!"})

    return render(request, "orders/edit_task_assignment.html", {
        "task": task,
        "workers": workers,
    })


@login_required
def view_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    po = invoice.po  

    # fetch order items that belong to this PO
    order_items = OrderItem.objects.filter(po=po)

    # add line_total for each item
    for item in order_items:
        qty = item.quantity or 0
        price = item.unit_price or 0
        item.line_total = qty * price

    grand_total = sum(item.line_total for item in order_items)

    return render(request, "invoices/view_invoice.html", {
        "invoice": invoice,
        "po": po,
        "order_items": order_items,
        'grand_total': grand_total,
    })


@login_required
def generate_invoice(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)

    # prevent duplicate invoices
    if hasattr(po, "invoice"):
        return redirect("managementSystem:view_invoice", invoice_id=po.invoice.id)

    # calculate total amount from order items
    items = OrderItem.objects.filter(po=po)
    total_amount = sum(item.unit_price * item.quantity for item in items)

    invoice = Invoice.objects.create(
        po=po,
        total_amount=total_amount,
        status="Pending"
    )

    return redirect("managementSystem:view_invoice", invoice_id=invoice.id)

def mark_invoice_paid(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.status = "Paid"
    invoice.save()
    return redirect("managementSystem:view_invoice", invoice_id=invoice.id)

def reports_view(request):
    today = now().date()
    view_type = request.GET.get("view_type", "daily")  # default = daily

    # Daily
    day = request.GET.get("day")
    if view_type == "daily":
        daily_orders = PurchaseOrder.objects.filter(date=day if day else today)
    else:
        daily_orders = []

    # Weekly
    if view_type == "weekly":
        week_day_str = request.GET.get("week_day")  # e.g. "2025-08-13"
        ref_date = datetime.strptime(week_day_str, "%Y-%m-%d").date() if week_day_str else today

        start_of_week = ref_date - timedelta(days=ref_date.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)                # Sunday

        weekly_orders = PurchaseOrder.objects.filter(date__range=[start_of_week, end_of_week])

        # optional: total value for the week (sum of all order items)
        val_expr = ExpressionWrapper(F("items__quantity") * F("items__unit_price"),
                                     output_field=DecimalField(max_digits=12, decimal_places=2))
        weekly_total_value = weekly_orders.aggregate(total=Sum(val_expr))["total"] or 0
    else:
        weekly_orders = PurchaseOrder.objects.none()
        start_of_week = end_of_week = None
        weekly_total_value = 0


    # Monthly
    month_str = request.GET.get("month")
    if view_type == "monthly":
        if month_str:
            year, month = month_str.split("-")
            monthly_orders = PurchaseOrder.objects.filter(date__year=int(year), date__month=int(month))
            current_month, current_year = int(month), int(year)
        else:
            monthly_orders = PurchaseOrder.objects.filter(date__year=today.year, date__month=today.month)
            current_month, current_year = today.month, today.year
    else:
        monthly_orders, current_month, current_year = [], today.month, today.year

    # Yearly
    year = request.GET.get("year")
    if view_type == "yearly":
        yearly_orders = PurchaseOrder.objects.filter(date__year=int(year)) if year else PurchaseOrder.objects.filter(date__year=today.year)
        current_year = int(year) if year else today.year
    else:
        yearly_orders, current_year = [], today.year

    return render(request, "reports.html", {
        "today": today,
        "daily_orders": daily_orders,
        "weekly_orders": weekly_orders,
        "monthly_orders": monthly_orders,
        "yearly_orders": yearly_orders,
        "current_month": current_month,
        "current_year": current_year,
        "active_tab": view_type,
        "weekly_total_value": weekly_total_value,
        "start_of_week": start_of_week,
        "end_of_week": end_of_week,
        "weekly_total_value": weekly_total_value,
    })

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRET_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
REDIRECT_URI = "http://127.0.0.1:8000/management/oauth2callback/"

FOLDER_NAME = "newleaf_backups"

def start_backup(request):
    """Step 1: Redirect user to Google consent screen"""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true', prompt='consent'
    )
    request.session['state'] = state
    return redirect(auth_url)


def oauth2callback(request):
    """Step 2: Handle Google redirect and upload DB file into folder"""
    state = request.session.get('state')

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI, state=state
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials
    service = build('drive', 'v3', credentials=creds)

    # --- Step 1: Check if backup folder exists ---
    query = f"mimeType='application/vnd.google-apps.folder' and name='{FOLDER_NAME}' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if items:
        folder_id = items[0]['id']
    else:
        file_metadata = {
            'name': FOLDER_NAME,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')

    # --- Step 2: Upload DB file into that folder ---
    file_metadata = {
        'name': 'db-backup.sqlite3',
        'parents': [folder_id]
    }
    media = MediaFileUpload('db.sqlite3', mimetype='application/x-sqlite3')
    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Success message
    messages.success(
        request,
        f"✅ Backup successfully uploaded to Google Drive folder '{FOLDER_NAME}'."
    )

    return redirect("dashboard:dashboard")