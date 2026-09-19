from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StudentGrade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grades', verbose_name='Учень')
    subject = models.CharField(max_length=100, verbose_name='Предмет')
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name='Оцінка')
    comment = models.TextField(blank=True, verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'

    def __str__(self): return f'{self.student.username} - {self.subject} - {self.grade}'
