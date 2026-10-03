from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    return redirect("poll_list")


urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("authentication.urls")),

    path("polls/", include("mypolls.urls")),

    path("", home, name="home"),
]