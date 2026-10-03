from django import forms
from .models import Gallery


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['file', 'media_type']
        labels = {
            'file': 'Файл',
            'media_type': 'Тип матеріалу',
        }