
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserCreationForm, UsernameField)
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "autocomplete": "first_name",
                "class": "form-control",
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "autocomplete": "last_name",
                "class": "form-control",
            }
        )
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Téléphone",
                "autocomplete": "phone_number",
                "class": "form-control",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )


    password1 = forms.CharField(
        label="Password",  # Ajouter de champ pour changer password1 en password
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "autocomplete": "new-password",
                "class": "form-control",
            }
        )
    )

    password2 = forms.CharField(
        label="Confirmation Password",  # Changement ici
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", 'phone', "password1", "password2",)



class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "autocomplete": "current-password",
                "class": "form-control",
            }
        )
    )