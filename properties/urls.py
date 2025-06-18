from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('delete/<int:pk>/', views.PropertyDeleteView.as_view(), name='delete_property'),
    path('add-property/', views.CreatePropertyView.as_view(), name='add_property'),
    path('update/<int:property_id>/', views.UpdatePropertyView.as_view(), name='update_property'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('detail/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('dashboard/', views.OwnerDashboardView.as_view(), name='owner_dashboard'),
    path("tenant/dashboard/", views.TenantDashboardView.as_view(), name="tenant_dashboard"),
]

