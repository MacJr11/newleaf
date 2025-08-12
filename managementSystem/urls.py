from django.urls import path
from . import views

app_name = 'managementSystem'
urlpatterns = [
    path('register_client/', views.register_client, name='register_client'),
    path('get/<int:pk>/', views.get_client, name='get_client'),
    path('delete/<int:pk>/', views.client_delete, name='client_delete'),
]
