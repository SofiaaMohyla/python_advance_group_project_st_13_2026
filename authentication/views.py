from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserProfileForm


# Create your views here.
class RegisterView(CreateView):
    template_name = 'authentication/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('notebook_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect('notebook_list')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'authentication/edit_profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self): return self.request.user
