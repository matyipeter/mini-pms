from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.views import View
from django.shortcuts import get_object_or_404
from users.models import OwnerProfile
from .models import Report 
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string


# Create your views here.

class ReportCreateView(View):

    """
    View to create a new report for the owner.
    The button will return to the ReportListView after creating the report.
    """

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

        return HttpResponseRedirect(reverse("reports:report_list"))

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
    
    # 1. Getting all data
    report = get_object_or_404(Report, pk=pk)

    # 2. Render HTML

    html_string = render_to_string(
        'reports/report_pdf.html',
        {
            'report': report,
        }
    )

    # 3. Generate PDF from HTML

    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # 4. Create HTTP response with PDF file

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="lease_report_id{report.pk}.pdf"'
    return response




