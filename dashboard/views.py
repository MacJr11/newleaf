from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper
from django.utils.timezone import now
from workers.models import Worker
from managementSystem.models import PurchaseOrder, OrderItem

@login_required
def dashboard_view(request):
    today = now().date()

    # Totals
    total_orders = PurchaseOrder.objects.count()
    completed_orders = PurchaseOrder.objects.filter(status="Completed").count()
    in_progress_orders = PurchaseOrder.objects.filter(status="In progress").count()
    pending_orders = PurchaseOrder.objects.filter(status="Pending").count()

    # Revenue calculation (based on completed orders)
    val_expr = ExpressionWrapper(F("items__quantity") * F("items__unit_price"),
                                 output_field=DecimalField(max_digits=12, decimal_places=2))
    total_revenue = PurchaseOrder.objects.filter(status="Completed").aggregate(
        total=Sum(val_expr)
    )["total"] or 0

    # Orders by month (for chart)
    orders_per_month = (
        PurchaseOrder.objects
        .values("date__year", "date__month")
        .annotate(count=Count("id"))
        .order_by("date__year", "date__month")
    )

    # Orders by status (for pie chart)
    orders_by_status = (
        PurchaseOrder.objects
        .values("status")
        .annotate(count=Count("id"))
    )

    # Recent orders
    if total_orders > 0:
        recent_orders = PurchaseOrder.objects.order_by("-date")[:5]
        pending_percent = round((pending_orders/total_orders)*100)
        completed_percent = round((completed_orders/total_orders)*100)
        inprogrs_percent = round((in_progress_orders/total_orders)*100)
    else:
        pending_percent = completed_percent = inprogrs_percent = recent_orders = 0

    top_workers = (
        Worker.objects.annotate(task_count=Count("taskassignment"))
        .order_by("-task_count")[:6]
    )

    # 🔥 Top 5 Clients (by number of purchase orders)
    top_clients = (
        PurchaseOrder.objects.values("client__id", "client__name", "client__address")
        .annotate(order_count=Count("id"))
        .order_by("-order_count")[:5]
    )

    return render(request, 'dashboard/index.html', {
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "in_progress_orders": in_progress_orders,
        "pending_orders": pending_orders,
        "pending_percent": pending_percent,
        "inprogress_percent": inprogrs_percent,
        "total_revenue": total_revenue,
        "completed_percent":completed_percent,
        "orders_per_month": list(orders_per_month),
        "orders_by_status": list(orders_by_status),
        "recent_orders": recent_orders,
        "today": today,
        "top_workers": top_workers,
        "top_clients": top_clients,
    })