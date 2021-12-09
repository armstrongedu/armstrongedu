import django.contrib.auth.forms  as auth_forms
from django.contrib.auth import get_user_model, password_validation
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class SignUpForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password',}
        )
        self.fields['password1'].help_text = password_validation.password_validators_help_texts()
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm Password',}
        )
        self.fields['password2'].help_text = _("Enter the same password as before, for verification."),


    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'email'}),
        }


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'email'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password',}
        )


class PasswordResetForm(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'email'}
        )

class SetPasswordForm(auth_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password',}
        )
        self.fields['new_password1'].help_text = password_validation.password_validators_help_texts()
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password',}
        )
        self.fields['new_password2'].help_text = _("Enter the same password as before, for verification."),
