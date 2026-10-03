from django.db import models
from django.conf import settings


class Poll(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        null = True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="Голосування"
    )
    text = models.CharField(max_length=200, verbose_name="Варіант")

    def __str__(self):
        return self.text


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Користувач"
    )
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        verbose_name="Голосування"
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        verbose_name="Вибір"
    )
    voted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "poll")

    def __str__(self):
        return f"{self.user} — {self.poll.title}"