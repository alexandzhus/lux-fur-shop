from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):
    """
    Тест модели User
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = get_user_model().objects.create(username='sashadzhus',
                                                        email='alexandrdzhus@gmail.com',
                                                        password='123',
                                                        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()

    def test_user_model_avatar_field_verbose_name(self) -> None:
        """
        Тест модели User, поля avatar на verbose_name
        :return: None
        """
        user = UserModelTestCase.test_user
        user_avatar_verbose_name = user._meta.get_field('avatar').verbose_name
        self.assertEqual(user_avatar_verbose_name, "Изображение пользователя")

    def test_user_model_avatar_field_upload_to(self) -> None:
        """
        Тест модели User, поля avatar на upload_to
        :return: None
        """
        user = UserModelTestCase.test_user
        user_avatar_upload_to = user._meta.get_field('avatar').upload_to
        self.assertEqual(user_avatar_upload_to, 'users/%Y/%m/%d/')

    def test_user_model_avatar_field_null(self) -> None:
        """
        Тест модели User, поля avatar на null
        :return: None
        """
        user = UserModelTestCase.test_user
        user_avatar_null = user._meta.get_field('avatar').null
        self.assertTrue(user_avatar_null)

    def test_user_model_avatar_field_blank(self) -> None:
        """
        Тест модели User, поля avatar на blank
        :return: None
        """
        user = UserModelTestCase.test_user
        user_avatar_blank = user._meta.get_field('avatar').blank
        self.assertTrue(user_avatar_blank)
