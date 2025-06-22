from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('create/', views.ReportCreateView.as_view(), name='report_create'),
    path('list/', views.ReportListView.as_view(), name='report_list'),
    #path('detail/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('download/<int:pk>/', views.report_download, name='report_pdf'),
]