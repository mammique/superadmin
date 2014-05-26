# -*- coding: utf-8 -*-
#from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.template import RequestContext
from django.contrib import messages

from .forms import UserForm


#@csrf_protect
def reception(request):

    if request.user.is_authenticated():

        form   = UserForm(instance=request.user)
        title  = 'Préférences'
        button = 'Modifier'

        if request.method == 'POST':

            form = UserForm(data=request.POST, instance=request.user)

            if form.is_valid():

                form.save()

                pwd = form.cleaned_data.get('password2')
                if pwd:
                    request.user.set_password(pwd)
                    request.user.save()
                    messages.success(request, 'Mot de passe modifié.')

                messages.success(request, 'Préférences modifiées.')

    else:

        title  = 'Login'
        button = 'Login'

        if request.method == 'POST':

            form = AuthenticationForm(data=request.POST)

            if form.is_valid():

                from django.contrib.auth import login
                user = form.get_user()
                login(request, user)
                form = UserForm(instance=user)

        else: form = AuthenticationForm()

    return render_to_response('reception.html', RequestContext(request, {'form': form, 'button': button, 'title': title}))


def logout_view(request):

    logout(request)

    return redirect('sa_auth:reception')
