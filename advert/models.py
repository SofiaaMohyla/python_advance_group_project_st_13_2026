from django.db import models
from django.utils import timezone
from authentication.models import CustomUser

class Advert(models.Model):
    class Priority(models.TextChoices):
        INFO = "info", "Інформаційне"
        REKLAMA = "reklama", "Рекламне"
        SOCIAL = "social", "Соціальне"
        ADMIN = "admin", "Адміністративне"

    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="adverts")    
    image = models.ImageField(
        upload_to="adverts/",
        verbose_name="Оголошення",
        default=""
    )
    datetime_from = models.DateTimeField(default=timezone.now) 
    datetime_to = models.DateTimeField(default=timezone.now) 
    priority = models.IntegerField(choices=Priority.choices, default=Priority.INFO)
    created_at = models.DateTimeField(auto_now_add=True)

