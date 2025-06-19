from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyCreateForm
from django.contrib.auth.decorators import login_required
from .models import Property
from django.views.generic.edit import CreateView, FormView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from users.models import OwnerProfile, TenantProfile
from datetime import date
from lease.models import Lease
from django.core.exceptions import PermissionDenied

class UpdatePropertyView(LoginRequiredMixin, FormView):
    form_class = PropertyCreateForm
    success_url = reverse_lazy('properties:success')
    template_name = 'properties/owner/update_property_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_owner:
            raise PermissionDenied("You are not an owner.")
        self.owner = OwnerProfile.objects.get(user=self.request.user)
        property_id = self.kwargs['property_id']
        try:
            self.property = Property.objects.get(id=property_id, owner=self.owner)
        except Property.DoesNotExist:
            raise PermissionDenied("You do not have permission to edit this property.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.property  # Prepopulate form with property data
        return kwargs

    def form_valid(self, form):
        # At this point, self.property is always the right property with the right owner
        self.owner.update_property(self.property.id, **form.cleaned_data)
        return super().form_valid(form)

class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'properties/success.html'

class OwnerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "properties/owner/owner_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = get_object_or_404(OwnerProfile, user=self.request.user)
        properties = Property.objects.filter(owner=owner)

        context['properties'] = properties
        context['property_count'] = properties.count()
        context['owner'] = owner
        return context

class TenantDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "properties/tenant/tenant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = get_object_or_404(TenantProfile, user=self.request.user)
        current_lease = Lease.objects.filter(tenant=tenant, is_active=True).first()
        context["current_lease"] = current_lease
        context["property"] = current_lease.property if current_lease else None
        return context

class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'properties/owner/property_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_lease = Lease.objects.filter(
            property=self.object,
        ).first()
        context["current_lease"] = current_lease
        return context

class CreatePropertyView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyCreateForm
    template_name = 'properties/owner/property_form.html'

    def form_valid(self, form):
        if self.request.user.is_owner:
            owner = OwnerProfile.objects.get(user=self.request.user)
            form.instance.owner = owner
        else:
            print("User is not owner")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("properties:owner_dashboard")

class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = "properties/owner/property_delete.html"
    context_object_name = "property"

    def get_success_url(self):
        return reverse_lazy("properties:owner_dashboard")