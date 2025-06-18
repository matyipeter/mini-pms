from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from users.forms import RegisterForm, LoginForm

# Create your views here.


class IndexPage(TemplateView):
    template_name = "users/index.html"


class RegisterView(FormView):
    template_name = "users/user_register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("users:index")  # Change this as needed

    def form_valid(self, form):
        user = form.save()

        user = authenticate(self.request, username=user.email, password=form.cleaned_data['password1'])

        if user is not None:
            # Manually set the backend used
            print("user not None")
            user.backend = 'users.backends.EmailBackend'  # <- use exact path
            login(self.request, user)

        return super().form_valid(form)
    
class LoginView(FormView):
    template_name = "users/user_login.html"
    form_class = LoginForm
    success_url = reverse_lazy("users:index")  # or any appropriate landing page

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid email or password.")
            return self.form_invalid(form)
