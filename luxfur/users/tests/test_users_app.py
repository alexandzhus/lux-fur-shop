from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase, Client

from django.urls import reverse


class UserAuthTestCase(TestCase):
    """
    Тестируем вход пользователя в систему
    """

    def setUp(self) -> None:
        """
        Метод создает тестового юзера. Вызывается перед каждым тестом.
        :return: None
        """
        self.user = get_user_model().objects.create_user(username='TestUser', email='test@example.com',
                                                         password='12test12')
        self.user.save()

    def tearDown(self) -> None:
        """
        Метод удаляет тестового юзера после каждого прошедшего теста.
        :return: None
        """
        self.user.delete()

    def test_correct(self) -> None:
        """
        Тест, который проверяет, что аутентификация пользователя прошла успешно
        :return: None
        """
        user = authenticate(username='TestUser', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self) -> None:
        """
        Тест, который проверяет, что аутентификация пользователя провалилась, из-за неправильного имени
        :return: None
        """
        user = authenticate(username='TestUser111', password='12test12')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_password(self) -> None:
        """
        Тест, который проверяет, что аутентификация пользователя провалилась, из-за неправильного пароля
        :return: None
        """
        user = authenticate(username='TestUser111', password='12test4565')
        self.assertFalse((user is not None) and user.is_authenticated)














