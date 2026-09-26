from django import forms
from  .models import Advert

class AdvertFilterForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "пошук"}))
    priority = forms.ChoiceField(required=False, choices=[("", "Будь-який")] + [(p.value, p.label) for p in Advert.Priority], widget=forms.Select(attrs={"class": "form-select"}))

class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert   
        fields = ["is_active", "priority", "datetime_from", "datetime_to", "title", "description", "image"]
        widgets = {
            "is_active": forms.Select(
                choices=[(True, "Так"), (False, "Ні")],
                attrs={"class": "form-select"}
            ),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "datetime_from": forms.DateTimeInput(attrs={"class": "form-control datepicker"}),
            "datetime_to": forms.DateTimeInput(attrs={"class": "form-control datepicker"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "image": forms.ClearableFileInput(attrs={"class": "form_control", "accept": "image/*"}),
        }
