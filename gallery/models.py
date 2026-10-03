from django.conf import settings
from django.db import models

MEDIA_TYPE_CHOICES = (
    ('photo', 'Фото'),
    ('video', 'Відео'),
)
class Gallery(models.Model):
    file = models.FileField(upload_to='gallery/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)