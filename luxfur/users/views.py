from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import *

class Login(LoginView):
    """
    Клас для авторизации пользователя
    """
    authentication_form = LoginUserForm
    template_name = 'users/login_form.html'
    extra_context = {
        'title': 'Авторизация'
    }

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin:index')

        return reverse_lazy('home')



