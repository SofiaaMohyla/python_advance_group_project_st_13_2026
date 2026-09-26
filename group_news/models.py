from django.db import models
from django.conf import settings

class News(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новини")
    image = models.ImageField(upload_to='news_photos/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title