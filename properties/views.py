from django.shortcuts import render, redirect
from .forms import PropertyCreateForm
from django.contrib.auth.decorators import login_required
from .models import Property
from django.views.generic.edit import CreateView, FormView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from users.models import OwnerProfile, TenantProfile, User
from django.shortcuts import get_object_or_404
from datetime import date
from lease.models import Lease

# Create your views here.


class UpdatePropertyView(FormView, LoginRequiredMixin):
    form_class = PropertyCreateForm
    success_url = reverse_lazy('properties:success')
    template_name = 'properties/update_property_form.html'


    def form_valid(self, form):
        if self.request.user.is_owner:
            user = self.request.user
            owner = OwnerProfile.objects.get(user=user)
        else:
            print("User is not owner")
            owner = None
        
        property_id = self.kwargs['property_id']
        owner.update_property(property_id, **form.cleaned_data)
        return super().form_valid(form)



class SuccessView(TemplateView, LoginRequiredMixin):
    template_name = 'properties/success.html'

############

class OwnerDashboardView(TemplateView):
    template_name = "properties/owner/owner_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current owner
        try:
            owner = get_object_or_404(OwnerProfile, user=self.request.user)
        except OwnerProfile.DoesNotExist:
            print("Owner not found")
            owner = None

        # Get the properties of the logged-in owner
        properties = Property.objects.filter(owner=owner)

        # Add context data for dashboard display
        context['properties'] = properties
        context['property_count'] = properties.count()
        context['owner'] = owner

        return context

class TenantDashboardView(TemplateView):
    template_name = "properties/tenant/tenant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = get_object_or_404(TenantProfile, user=self.request.user)

        current_lease = Lease.objects.filter(tenant=tenant, is_active=True).first()
        context["current_lease"] = current_lease
        context["property"] = current_lease.property if current_lease else None
        return context


class PropertyDetailView(DetailView, LoginRequiredMixin):
    model = Property
    template_name = 'properties/owner/property_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        current_lease = Lease.objects.filter(
            property=self.object,
        ).first()
        context["current_lease"] = current_lease
        return context


class CreatePropertyView(CreateView, LoginRequiredMixin):
    model = Property
    form_class = PropertyCreateForm
    template_name = 'properties/owner/property_form.html'

    def form_valid(self, form):
        if(self.request.user.is_owner):
            owner = OwnerProfile.objects.get(user=self.request.user)
            form.instance.owner = owner
        else:
            print("User is not owner")
            owner = None

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("properties:owner_dashboard")


class PropertyDeleteView(DeleteView):
    model = Property
    template_name = "properties/owner/property_delete.html"
    context_object_name = "property"

    def get_success_url(self):
        return reverse_lazy("properties:owner_dashboard")