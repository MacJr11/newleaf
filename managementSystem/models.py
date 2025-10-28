from django.db import models
from workers.models import Worker
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal


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
    order_no = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')

    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} ({self.quantity})"
    
    @property
    def gross(self):
        return self.quantity * self.unit_price



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
            if self.workers.count() == 0:
                return 0
            total_pay = self.price_per_task * count
            return round(total_pay / self.workers.count(), 2)
        else:
            return float(self.price_per_task)


    def __str__(self):
        return f"Task for: {self.order_item}"

class Invoice(models.Model):
    po = models.OneToOneField(PurchaseOrder, on_delete=models.CASCADE, related_name="invoice")
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid")],
        default="Pending"
    )

    def __str__(self):
        return f"Invoice for PO {self.po.id} - {self.status}"

class VATInvoice(models.Model):
    purchase_order = models.OneToOneField(PurchaseOrder, on_delete=models.CASCADE, related_name="vat_invoice")
    invoice_number = models.CharField(max_length=50, unique=True)
    date_issued = models.DateTimeField(auto_now_add=True)

    gross = models.DecimalField(max_digits=12, decimal_places=2)
    nhil = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    getfund_levy = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    covid_levy = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_levy = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        nhil_rate = Decimal("2.5") / Decimal("100")
        getfund_rate = Decimal("2.5") / Decimal("100")
        covid_rate = Decimal("1") / Decimal("100")
        vat = Decimal("15") / Decimal("100")

        self.nhil = self.gross * nhil_rate
        self.getfund_levy = self.gross * getfund_rate
        self.covid_levy = self.gross * covid_rate
        self.total_levy = self.nhil + self.getfund_levy + self.covid_levy + self.gross
        self.vat = self.total_levy * vat
        self.total_amount = self.total_levy + self.vat
        super().save(*args, **kwargs)

    def __str__(self):
        return f"VAT Invoice {self.invoice_number} for {self.purchase_order.po_number}"
   


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"



class ProformaInvoice(models.Model):
    po_number = models.CharField(max_length=50, unique=True, blank=True)
    client_name = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.po_number:
            # Generate unique number like PF-20251004-001
            today = timezone.now().strftime("%Y%m%d")
            last = ProformaInvoice.objects.filter(po_number__startswith=f"PF-{today}").count() + 1
            self.po_number = f"PF-{today}-{last:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Proforma Invoice {self.po_number}"

class ProformaItem(models.Model):
    invoice = models.ForeignKey(ProformaInvoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} - {self.invoice.po_number}"