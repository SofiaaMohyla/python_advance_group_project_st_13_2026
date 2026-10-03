from django.urls import path
from .views import gallery, upload_gallery, delete_gallery, manage_uploads

urlpatterns = [
    path('', gallery, name='gallery'),
    path('upload/', upload_gallery, name='upload_gallery'),
    path('delete/<int:pk>/', delete_gallery, name='delete_gallery'),
    path('manage-uploads/', manage_uploads, name='manage_uploads'),
]