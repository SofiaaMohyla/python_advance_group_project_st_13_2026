from django import forms
from .models import Poll


class PollForm(forms.ModelForm):
    choices = forms.CharField(
        label="Варіанти відповідей",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Введіть кожен варіант з нового рядка"
            }
        ),
        help_text="Кожен варіант відповіді введіть з нового рядка."
    )

    class Meta:
        model = Poll
        fields = ["title", "description"]
        labels = {
            "title": "Назва голосування",
            "description": "Опис",
        }