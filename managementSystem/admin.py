from django.contrib import admin
from .models import Client, PurchaseOrder, OrderItem, TaskAssignment


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
