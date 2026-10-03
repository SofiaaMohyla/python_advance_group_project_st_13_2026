from datetime import datetime, time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserProfileForm
from events_calendar.models import Event


# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.template_name == 'events-calendar.html':
            context['events'] = Event.objects.all().order_by('start_time')
        return context


def manager_required(view):
    def wrapped_view(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.role in {'moderator', 'admin'}):
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return wrapped_view


@login_required
@manager_required
def create_event(request):
    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.POST['start_time'], '%Y-%m-%d').date()
            end_date = datetime.strptime(request.POST['end_time'], '%Y-%m-%d').date()
        except (KeyError, ValueError):
            return render(request, 'create-event.html', {
                'error': 'Вкажіть коректні дати початку та закінчення.'
            })

        if end_date < start_date:
            return render(request, 'create-event.html', {
                'error': 'Дата закінчення не може бути раніше дати початку.'
            })

        Event.objects.create(
            title=request.POST.get('title', '').strip(),
            description=request.POST.get('description', '').strip(),
            start_time=timezone.make_aware(datetime.combine(start_date, time.min)),
            end_time=timezone.make_aware(datetime.combine(end_date, time.min)),
            location=request.POST.get('location', '').strip(),
        )
        return render(request, 'create-event.html', {'created': True})

    return render(request, 'create-event.html')


@login_required
@manager_required
def edit_event(request):
    events = Paginator(Event.objects.all().order_by('start_time'), 10).get_page(
        request.GET.get('page')
    )
    event_id = request.POST.get('event_id') or request.GET.get('event_id')
    selected_event = get_object_or_404(Event, pk=event_id) if event_id else None

    if request.method == 'POST' and selected_event:
        selected_event.title = request.POST.get('title', '').strip()
        selected_event.description = request.POST.get('description', '').strip()
        selected_event.location = request.POST.get('location', '').strip()
        selected_event.save(update_fields=['title', 'description', 'location'])
        return redirect(f'{request.path}?event_id={selected_event.id}')

    return render(request, 'edit-event.html', {
        'events': events,
        'selected_event': selected_event,
    })


@login_required
@manager_required
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        event.delete()

    return redirect('edit_event')
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

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['can_edit_role'] = (
            self.request.user.is_superuser or self.request.user.role == 'admin'
        )
        return kwargs
    def get_object(self): return self.request.user
