from django.contrib import admin
from .models import *

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'role', 'registered_on')
    search_fields = ('name', 'phone')

@admin.register(WorkerPayment)
class WorkerPaymentAdmin(admin.ModelAdmin):
    list_display = ('worker', 'amount', 'method', 'payment_date')
    search_fields = ('worker', 'Payment_date')