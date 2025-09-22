from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, PurchaseOrder

@receiver(post_save, sender=OrderItem)
def  update_purchase_order_status(sender, instance, **kwargs):
    po = instance.po
    items = po.items.all()

    if all(item.status == "Completed" for item in items):
        po.status = "Completed"
    elif any(item.status in ["In progress", "Completed"] for item in items):
        po.status = "In progress"
    else: 
        po.status = "Pending"

    po.save(update_fields=["status"])