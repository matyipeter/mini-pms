from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.views import View
from django.shortcuts import get_object_or_404
from users.models import OwnerProfile
from .models import Report 
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

class ReportCreateView(View):

    def post(self, request):
        user = request.user
        owner = get_object_or_404(OwnerProfile, user=user)

        report = Report.objects.create(
            owner=owner,
            number_of_properties=owner.properties.count(),
            number_of_tenants=self.calc_tenants(owner),
            monthly_income=self.calc_income(owner),
            monthly_expenses=0.00,
            available_properties=owner.properties.filter(occupancy_status="available").count(),
            occupied_properties=owner.properties.filter(occupancy_status="occupied").count()
        )

        report.save()

        return HttpResponseRedirect(reverse("properties:owner_dashboard"))

    def calc_tenants(self, owner):
        count = 0
        for prop in owner.properties.all():
            if prop.get_current_lease() != None:
                if prop.get_current_lease().is_active:
                    count += 1
        return count
    
    def calc_income(self, owner):
        income = 0
        for prop in owner.properties.all():
            lease = prop.get_current_lease()
            if lease != None and lease.is_active:
                income += lease.rent_amount
        return income


class ReportListView(ListView):
    model = Report
    template_name = "reports/report_list.html"
    context_object_name = "reports"

    def get_queryset(self):
        user = self.request.user
        owner = get_object_or_404(OwnerProfile, user=user)
        return Report.objects.filter(owner=owner).order_by('-created_at')


def report_download(request, pk):
    report = get_object_or_404(Report, pk=pk)
    
    # Here you would implement the logic to generate a downloadable report file
    # For simplicity, we will just return a simple text response
    # PDF creating will be added using WeasyPrint
    response = HttpResponse(
        f"Report for {report.owner.user.username} - {report.created_at.strftime('%Y-%m-%d')}\n"
        f"Number of Properties: {report.number_of_properties}\n"
        f"Number of Tenants: {report.number_of_tenants}\n"
        f"Monthly Income: {report.monthly_income}\n"
        f"Monthly Expenses: {report.monthly_expenses}\n"
        f"Available Properties: {report.available_properties}\n"
        f"Occupied Properties: {report.occupied_properties}",
        content_type='text/plain'
    )
    response['Content-Disposition'] = f'attachment; filename="report_{pk}.txt"'
    
    return response




