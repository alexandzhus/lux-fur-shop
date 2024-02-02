from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest


class EmailAuthBackend(BaseBackend):
    """
    Клас будет использоваться для аутентификации пользователя по емейлу
    """

    def authenticate(self, request: HttpRequest, username=None, password=None, **kwargs):
        """
        Используется для аутентификации пользователя возвращает либо None, или объект пользователя
        :param request: HttpRequest
        :param username:
        :param password:
        :return:
        """
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """
        Метод используется для получения юзера из базы
        :param user_id:
        :return:
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
