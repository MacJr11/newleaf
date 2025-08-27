from django.db import models
from django.utils import timezone

class Worker(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True)
    role = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    photo = models.ImageField(upload_to='img/users/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    registered_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    
class WorkerPayment(models.Model):
    CASH = "cash"
    MOMO = "momo"
    BANK = "bank"

    METHOD_CHOICES = [
        (CASH, "Cash"),
        (MOMO, "Mobile Money"),
        (BANK, "Bank Transfer"),
    ]

    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default=MOMO)
    reference = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.worker.name} - {self.amount} on {self.payment_date}"
