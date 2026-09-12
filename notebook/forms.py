from django import forms
from .models import StudentGrade

class StudentGradeForm(forms.ModelForm):
    class Meta:
        model = StudentGrade
        fields = ['student', 'subject', 'grade', 'comment']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: Математика'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Коментар до оцінки'}),
        }
