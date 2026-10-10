from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path
from .views import ProfileUpdateView, HomeView, create_event, delete_event, edit_event

from django.urls import path, include
from .views import RegisterView, ProfileUpdateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),


    path('events/', HomeView.as_view(template_name='events-calendar.html'), name='events'),
    path('register_event/', HomeView.as_view(template_name='register-event.html'), name='register_event'),

    path('create_event/', create_event, name='create_event'),
    path('edit_event/', edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', delete_event, name='delete_event'),






    path('', include('advert.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

