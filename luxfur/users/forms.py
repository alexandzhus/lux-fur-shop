from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    """
    Класс формы для отображения полей модели user.
    Используется для аутнтификации пользователей.
    """

    username = forms.CharField(max_length=255, label="Логин")
    password = forms.CharField(label="Пароль")

    class Meta:
        model = get_user_model()
        field = ['username', 'password']