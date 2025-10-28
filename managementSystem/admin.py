from django.contrib import admin
from .models import Client, PurchaseOrder, OrderItem, TaskAssignment, Notification, VATInvoice, ProformaInvoice, ProformaItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'client', 'date', 'due_date', 'status')
    inlines = [OrderItemInline]
    list_filter = ('status', 'date', 'due_date')
    search_fields = ('po_number', 'client__name')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'contact_email')
    search_fields = ('name', 'phone')



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('po', 'description', 'quantity', 'unit_price', 'status')
    search_fields = ('description', 'po')


@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'deadline', 'is_group_task', 'price_per_task', 'status')
    filter_horizontal = ('workers',)
    list_filter = ('status', 'is_group_task')

@admin.register(Notification)
class Notification(admin.ModelAdmin):
    list_display = ('user', 'title', 'message', 'created_at', 'is_read')
    list_filter = ('created_at', 'is_read')

@admin.register(VATInvoice)
class VATInvoice(admin.ModelAdmin):
    list_display = ('invoice_number', 'purchase_order', 'gross', 'date_issued', 'total_levy', 'vat', 'total_amount')
    list_filter = ('date_issued', 'gross')

@admin.register(ProformaInvoice)
class ProformaInvoice(admin.ModelAdmin):
    list_display = ('client_name', 'po_number', 'date')
    list_filter = ('client_name', 'date')

@admin.register(ProformaItem)
class ProformaItem(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price')
    list_filter = ('invoice', 'description')
