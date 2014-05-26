# -*- coding: utf-8 -*-

# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#a-full-example
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as UserAdminDjango
from django.contrib.auth.forms import UserChangeForm as UserChangeFormDjango
from django.contrib.auth.forms import AdminPasswordChangeForm as AdminPasswordChangeFormDjango
from django.utils.translation import ugettext, ugettext_lazy as _

from sa_auth.models import User


# https://github.com/django/django/blob/ed4c2e1c0d9e43c09767b02fd8b4bd74a5dfe512/django/contrib/auth/forms.py#L70
class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'godfathers',)


class UserChangeForm(UserChangeFormDjango):

    class Meta:
        model = User


class UserAdmin(UserAdminDjango):
    # The forms to add and change user instances
    form                 = UserChangeForm
    add_form             = UserCreationForm
    change_password_form = AdminPasswordChangeFormDjango

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser',) # , 'godfathers'
    list_filter  = ('is_superuser',)
    fieldsets    = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password')}),
        ('Personal info', {'fields': ('godfathers',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'godfathers', 'password1', 'password2')}
        ),
    )
    search_fields     = ('username', 'first_name', 'last_name', 'email',)
    ordering          = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
