from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from .forms import StudentGradeForm
from .models import StudentGrade


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.role == 'admin')


class StudentGradeListView(LoginRequiredMixin, ListView):
    model = StudentGrade
    template_name = 'notebook/gradebook_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return StudentGrade.objects.select_related('student').order_by('-updated_at')


class StudentGradeCreateView(AdminRequiredMixin, CreateView):
    model = StudentGrade
    form_class = StudentGradeForm
    template_name = 'notebook/gradebook_form.html'
    success_url = reverse_lazy('notebook_list')


class StudentGradeUpdateView(AdminRequiredMixin, UpdateView):
    model = StudentGrade
    form_class = StudentGradeForm
    template_name = 'notebook/gradebook_form.html'
    success_url = reverse_lazy('notebook_list')


class StudentGradeDeleteView(AdminRequiredMixin, DeleteView):
    model = StudentGrade
    template_name = 'notebook/gradebook_confirm_delete.html'
    success_url = reverse_lazy('notebook_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
