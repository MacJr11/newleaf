from django.urls import path
from . import views

app_name = 'workers'
urlpatterns = [
    path('', views.worker_list, name='worker_list'),
    path('search/', views.worker_search, name='worker_search'),
    path('get/<int:pk>/', views.get_worker, name='get_worker'),
    path('delete/<int:pk>/', views.worker_delete, name='worker_delete'),
]
