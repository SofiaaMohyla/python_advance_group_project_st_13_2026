from django import forms
from .models import ForumMessage

class ForumMessageForm(forms.ModelForm):
    class Meta:
        model = ForumMessage
        fields = ['title', 'text']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть заголовок'
            }),

            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть текст повідомлення',
                'rows': 6
            }),
        }

        def clean_title(self):
            title = self.cleaned_data.get('title')
            if len(title) < 5:
                raise forms.ValidationError("Title must be at least 5 characters long.")
            return title

        def clean_text(self):
            text = self.cleaned_data.get('text')
            if len(text) < 10:
                raise forms.ValidationError("Text must be at least 10 characters long.")
            return text