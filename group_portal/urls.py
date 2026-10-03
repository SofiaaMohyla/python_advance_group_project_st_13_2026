from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('', include("authentication.urls")),
    path('forum/', include("forum.urls")),
    path('gallery/', include('gallery.urls')),
    path('', include('authentication.urls')),
    path('notebook/', include('notebook.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
from django.shortcuts import redirect


def home(request):
    return redirect("poll_list")


urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("authentication.urls")),

    path("polls/", include("mypolls.urls")),

    path("", home, name="home"),
]
>>>>>>> golosovania
