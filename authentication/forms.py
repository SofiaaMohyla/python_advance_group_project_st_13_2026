from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError('Користувач із таким іменем уже існує.')
        return username

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, can_edit_role=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not can_edit_role:
            self.fields.pop('role', None)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
