from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from config import settings
from .forms import *

class Login(LoginView):
    """
    Клас для авторизации пользователя.
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


class RegisterUser(CreateView):
    """
    Клас используется для регистрации нового пользователя.
    """

    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")
    extra_context = {
        'title': 'Регистрация нового пользователя'
    }


class ProfileUser(UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': 'Профиль пользователя',
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        """
        Для переадресации в случае успешного изменения в профиле
        :return:
        """
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user