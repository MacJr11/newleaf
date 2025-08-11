from django.contrib import admin
from .models import Worker

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'role', 'registered_on')
    search_fields = ('name', 'phone')
