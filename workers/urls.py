from django.urls import path
from . import views

app_name = 'workers'
urlpatterns = [
    path('', views.worker_list, name='worker_list'),
    path('search/', views.worker_search, name='worker_search'),
    path('get/<int:pk>/', views.get_worker, name='get_worker'),
    path('delete/<int:pk>/', views.worker_delete, name='worker_delete'),
    path("profile/<int:worker_id>/", views.worker_profile, name="worker_profile"),
    path("profile/<int:worker_id>/pay/", views.record_payment, name="record_payment"),
]
