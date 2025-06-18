from django.urls import path
from . import views

app_name = 'lease'

urlpatterns = [
    path('detail/<int:pk>/', views.LeaseDetailView.as_view(), name='lease_detail'),
    path('create/<int:property_id>/', views.CreateLeaseView.as_view(), name='create_lease'),
    path('terminate/<int:pk>/', views.TerminateLeaseView.as_view(), name='terminate_lease'),
    path("terminate/confirm/<int:pk>", views.LeaseTerminateConfirmView.as_view(), name="lease_terminate_confirm"),
    path("tenant/<int:pk>/", views.TenantLeaseDetailView.as_view(), name="tenant_lease_detail"),
]
