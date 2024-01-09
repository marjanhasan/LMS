from . import forms
from books.models import PurchaseHistoryModel
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = "form.html"
    success_url = reverse_lazy("login")
    form_class = forms.RegistrationForm
    success_message = "Your account created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Register"
        return context


class UserLoginView(LoginView):
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "You are successfully logged in")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Email/Password is incorrect")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Login"
        return context


@method_decorator(login_required, name="dispatch")
class UserLogoutView(LogoutView):
    template_name = "logout.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, "Logged out successfully!")
        return response


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        data = PurchaseHistoryModel.objects.filter(user=request.user)
        return render(request, "profile.html", {"data": data})


@method_decorator(login_required, name="dispatch")
class EditPassword(PasswordChangeView):
    template_name = "update.html"
    success_url = reverse_lazy("profile")
    success_message = "Password changed successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


@login_required
def edit_profile(request):
    if request.method == "POST":
        profile_form = forms.ChangeUserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")

    else:
        profile_form = forms.ChangeUserForm(instance=request.user)
    return render(request, "update.html", {"form": profile_form})
