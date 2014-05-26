# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import ugettext, ugettext_lazy as _


class User(AbstractUser):

    godfathers = models.ManyToManyField('self', null=True, blank=True,
                     symmetrical=False, related_name='nephews')

    def set_password(self, pwd):

        # Set pwd here.

        return super(User, self).set_password(pwd)

User._meta.get_field("first_name").blank = False
User._meta.get_field("last_name").blank  = False
User._meta.get_field("email").blank      = False
