from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, UpdateView
from django.views import View
from .models import Lease
from django.views.generic.edit import CreateView
from .forms import LeaseForm
from properties.models import Property
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django import forms
from django.views.generic import TemplateView
from users.models import TenantProfile

class LeaseDetailView(DetailView):
    model = Lease
    template_name = "lease/lease_detail.html"
    context_object_name = "lease"


class CreateLeaseView(CreateView):
    model = Lease
    form_class = LeaseForm
    template_name = "lease/lease_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.property = get_object_or_404(Property, pk=kwargs["property_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["property"].initial = self.property
        form.fields["property"].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["property"] = self.property
        return context

    def form_valid(self, form):
        form.instance.property = self.property
        form.instance.set_active()
        form.instance.tenant = form.cleaned_data["tenant"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("lease:lease_detail", kwargs={"pk": self.object.pk})


class TerminateLeaseView(View):
    
    def post(self, request, pk):
        lease = get_object_or_404(Lease, pk=pk)

        lease.terminate()
        lease.property.occupancy_status = 'Available'
        lease.property.save()
        return redirect(reverse("lease:lease_detail", kwargs={"pk": lease.pk}))

class LeaseTerminateConfirmView(TemplateView):
    template_name = "lease/lease_terminate_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lease = get_object_or_404(Lease, pk=self.kwargs["pk"])
        context["lease"] = lease
        return context


class TenantLeaseDetailView(DetailView):
    model = Lease
    template_name = "lease/tenant_lease_detail.html"
    context_object_name = "lease"

    def get_queryset(self):
        # Only allow access to the tenant's own lease
        tenant = get_object_or_404(TenantProfile, user=self.request.user)
        return Lease.objects.filter(tenant=tenant)
    