from django.db import models
from workers.models import Worker

class Client(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.po_number


class OrderItem(models.Model):
    po = models.ForeignKey(PurchaseOrder, related_name='items', on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} ({self.quantity})"


class TaskAssignment(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    workers = models.ManyToManyField(Worker)
    deadline = models.DateField()
    is_group_task = models.BooleanField(default=True)
    price_per_task = models.DecimalField(max_digits=10, decimal_places=2)  # user-defined price per task
    status = models.CharField(max_length=20, default='Assigned')

    def calculate_payments(self):
        count = self.order_item.quantity
        if self.is_group_task:
            total_pay = self.price_per_task * count
            return round(total_pay / self.workers.count(), 2)
        else:
            return float(self.price_per_task)

    def __str__(self):
        return f"Task for: {self.order_item}"

