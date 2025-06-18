from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('request/', views.MaintenanceRequestCreateView.as_view(), name='maintenance_request'),
]
    