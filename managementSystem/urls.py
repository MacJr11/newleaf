from django.urls import path
from . import views

app_name = 'managementSystem'
urlpatterns = [
    path('register_client/', views.register_client, name='register_client'),
    path('get/<int:pk>/', views.get_client, name='get_client'),
    path('delete/<int:pk>/', views.client_delete, name='client_delete'),
    path('purchase_orders/', views.orders, name='orders'),
    path('add_purchase_orders/', views.create_order, name='create_order'),
    path('purchase-order/<int:po_id>/', views.view_po, name='view_po'),
    path('purchase-order/<int:po_id>/add-item/', views.add_order_item, name='add_order_item'),
]
