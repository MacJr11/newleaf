from django.db import models

class Worker(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=100)
    registered_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name