from django.urls import path
from . import views

app_name = 'managementSystem'
urlpatterns = [
    path('register_client/', views.register_client, name='register_client'),
    path('get/<int:pk>/', views.get_client, name='get_client'),
    path('delete/<int:pk>/', views.client_delete, name='client_delete'),
    path('purchase_orders/', views.orders, name='orders'),
    path('add_purchase_orders/', views.create_order, name='create_order'),
    path('edit_purchase_orders/<int:po_id>/', views.edit_po, name='edit_po'),
    path('purchase-order/<int:po_id>/', views.view_po, name='view_po'),
    path('purchase-order/<int:po_id>/add-item/', views.add_order_item, name='add_order_item'),
    path('po/<int:po_id>/assign-workers/', views.assign_workers, name='assign_workers'),
    path("edit_order_item/<int:item_id>/", views.edit_order_item, name="edit_order_item"),
    path("delete_order_item/<int:item_id>/", views.delete_order_item, name="delete_order_item"),
    path("edit_task_assignment/<int:task_id>/", views.edit_task_assignment, name="edit_task_assignment"),
    path('search/', views.po_search, name='po_search'),
]
