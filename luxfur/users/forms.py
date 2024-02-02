from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
    """
    Класс формы для отображения полей модели user.
    Используется для аутнтификации пользователей.
    """

    username = forms.CharField(max_length=255, label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        field = ['username', 'password']



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует")
        return email



class UserProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин')
    email = forms.CharField(disabled=True, label="E-mail")

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'avatar', 'first_name', 'last_name']
        labels = {
            'avatar': 'Аватар пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }


