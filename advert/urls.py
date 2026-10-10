from django.urls import path
from advert import views

urlpatterns = [
    path("advert/my/list/", views.AdvertListOwner.as_view(), name="advert_owner_list"),
    path("advert/list/", views.AdvertList.as_view(), name="advert_all_list"),
    path("advert/create/", views.AdvertCreate.as_view(), name="advert_create"),
    path("advert/detail/<slug:slug>/", views.AdvertDetail.as_view(), name="advert_detail"),
    path("advert/delete/<slug:slug>/", views.AdvertDelete.as_view(), name="advert_delete"),    
    path("advert/update/<slug:slug>/", views.AdvertUpdate.as_view(), name="advert_update"),  
]