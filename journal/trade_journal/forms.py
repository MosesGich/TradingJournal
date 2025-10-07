from django import forms
from .models import Trade
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email address",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"})
    )

    first_name = forms.CharField(
        required=True,
        max_length=60,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"})
    )

    last_name = forms.CharField(
        required=True,
        max_length=60,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "last name"})
    )

    accept_terms = forms.BooleanField(
        required=True,
        label="I agree to terms and services"
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "accept_terms")
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("email already in use")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        
        if commit:
            user.save()
        return user
class TradeForm(forms.ModelForm):
    class Meta():
        model = Trade
        fields = ["image", "outcome", "pair", "profit", "date", "notes"]
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'} # This renders <input type="date">
            )
        }