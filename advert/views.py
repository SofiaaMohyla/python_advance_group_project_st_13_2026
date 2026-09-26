from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserIsOwnerMixin
from .models import Advert
from django.db.models import Q
from .forms import AdvertFilterForm, AdvertForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.conf import settings

# Create your views here.
class AdvertListOwner(LoginRequiredMixin, ListView):
    model = Advert
    template_name = "advert/owner_list.html"
    context_object_name = "adverts"
    paginate_by = 5

    def get_queryset(self):
        all = Advert.objects.filter(author=self.request.user)
        q = self.request.GET.get("q") or ""
        priority = self.request.GET.get("priority") or ""
        if q:
            all = all.filter(Q(name_icontains=q))
        if priority:
            all = all.filter(priority=priority)

        return all.select_related("author") 

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = AdvertFilterForm(self.request.GET or None)
        return ctx           

class AdvertList(ListView):
    model = Advert
    template_name = "advert/all_list.html"
    context_object_name = "adverts"
    paginate_by = 5

    def get_queryset(self):
        now = timezone.now()
        all = Advert.objects.filter(is_active=True, datetime_from__lte=now, datetime_to__gte=now)
        q = self.request.GET.get("q") or ""
        priority = self.request.GET.get("priority") or ""
        if q:
            all = all.filter(Q(name_icontains=q))
        if priority:
            all = all.filter(priority=priority)

        return all.select_related("author") 

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = AdvertFilterForm(self.request.GET or None)
        return ctx           

class AdvertCreate(LoginRequiredMixin, CreateView):
    model = Advert
    form_class = AdvertForm 
    template_name = "advert/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("advert_detail", kwargs={"slug": self.object.id})

class AdvertDetail(DetailView):
    model = Advert
    template_name = "advert/detail.html"
    context_object_name = "advert"
    slug_field = "id"
    slug_url_kwarg = "slug"    


class AdvertDelete(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Advert
    template_name = "advert/confirm_delete.html"
    slug_field = "id"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("advert_owner_list")

class AdvertUpdate(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Advert
    form_class = AdvertForm
    template_name = "advert/create.html"
    slug_field = "id"
    slug_url_kwarg = "slug" 
    
    def get_success_url(self):
        return reverse_lazy("advert_detail", kwargs={"slug": self.object.id})    