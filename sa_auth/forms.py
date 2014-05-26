# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import User


class UserForm(ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Nouveau mot de passe"), required=False,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Nouveau mot de passe (confirmer)"), required=False,
                                widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    class Meta:

        model = User
        fields = ('first_name', 'last_name', 'email',)
