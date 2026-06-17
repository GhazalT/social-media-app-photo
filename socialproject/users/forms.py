from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "field-input",
                "placeholder": "First name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "field-input",
                "placeholder": "Last name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "field-input",
                "placeholder": "you@example.com",
            }),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("photo", "bio")
        widgets = {
            "photo": forms.ClearableFileInput(attrs={
                "class": "field-input field-input--file",
                "data-image-input": "",
            }),
            "bio": forms.Textarea(attrs={
                "class": "field-input",
                "placeholder": "Tell people what you like to post",
                "rows": 3,
            }),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "field-input",
        "autocomplete": "username",
        "placeholder": "Your username",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "field-input",
        "autocomplete": "current-password",
        "placeholder": "Your password",
    }))


class UserRegistartionForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "field-input",
        "autocomplete": "email",
        "placeholder": "you@example.com",
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "class": "field-input",
        "autocomplete": "new-password",
        "placeholder": "Choose a password",
    }))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        "class": "field-input",
        "autocomplete": "new-password",
        "placeholder": "Repeat your password",
    }))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "field-input",
                "autocomplete": "username",
                "placeholder": "Pick a username",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "field-input",
                "autocomplete": "given-name",
                "placeholder": "First name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "field-input",
                "autocomplete": "family-name",
                "placeholder": "Last name",
            }),
        }

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


