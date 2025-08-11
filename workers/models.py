from django.db import models

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