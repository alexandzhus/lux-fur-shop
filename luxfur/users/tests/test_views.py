from django.contrib.auth import authenticate
from django.test import TestCase, RequestFactory
from django.urls import reverse

from users.views import *


class LoginViewTestCase(TestCase):
    """
    Тесты для представления Login приложения users
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = get_user_model().objects.create(username='sashadzhus',
                                                        email='alexandrdzhus@gmail.com',
                                                        password='123',
                                                        )
        cls.test_user.save()
        cls.view = Login()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()




    def test_views_url_path_exists(self) -> None:
        """
        Тест представления Login на существующий url-path
        :return: None
        """
        response = self.client.get('/users/login/')
        res = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res.status_code, 200)

    def test_view_get_right_context(self) -> None:
        """
        Тест представления Login, что передается правильный контекст
        :return: None
        """

        context_auth_form = self.view.authentication_form
        extra_context = self.view.extra_context
        self.assertEqual(context_auth_form, LoginUserForm)
        self.assertEqual(extra_context, {'title': 'Авторизация'})


    def test_views_use_right_template(self) -> None:
        """
        Тест представления Login использует правильный шаблон
        :return: None
        """
        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response, 'users/login_form.html')



class RegisterUserViewTestCase(TestCase):
    """
    Тест представления RegisterUser
    """

    def test_view_url_path_exists(self) -> None:
        """
        Тест представления RegisterUser на существование url-path
        :return: None
        """
        response_url = self.client.get('/users/register/')
        response_url_name = self.client.get(reverse('users:register'))
        self.assertEqual(response_url.status_code, 200)
        self.assertEqual(response_url_name.status_code, 200)

    def test_view_user_right_template(self) -> None:
        """
        Тест представления RegisterUser на использование правильного шаблона
        :return: None
        """
        response = self.client.get(reverse('users:register'))
        self.assertTemplateUsed(response, 'users/register.html')

    def test_view_give_right_context(self) -> None:
        """
        Тест представления RegisterUser на получение правильного контекста
        :return: None
        """
        view = RegisterUser()
        view_extra_context = view.extra_context
        self.assertEqual(view_extra_context, {'title': 'Регистрация нового пользователя'})

    def test_view_use_right_form(self) -> None:
        """
        Тест представления RegisterUser на получение правильной формы
        :return: None
        """
        view = RegisterUser()
        view_form_class = view.form_class
        self.assertEqual(view_form_class, UserRegisterForm)

    def test_view_use_right_reverse(self) -> None:
        """
        Тест представления RegisterUser на получение правильного пути перенаправления
        :return: None
        """
        view = RegisterUser()
        view_success_url = view.success_url
        self.assertEqual(view_success_url, reverse_lazy("users:login"))





class ProfileUserViewTestCase(TestCase):
    """
    Тест представления ProfileUser
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = get_user_model().objects.create(username='sashadzhus',
                                                        email='alexandrdzhus@gmail.com',
                                                        password='123',
                                                        )
        cls.view = ProfileUser()
        cls.test_user.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()

    def setUp(self):
        self.client.force_login(self.test_user)

    def test_view_url_path_exists(self) -> None:
        """
        Тест представления ProfileUser на существование url-path
        :return: None
        """
        response_url = self.client.get('/users/profile/')
        response_url_name = self.client.get(reverse('users:profile'))
        self.assertEqual(response_url.status_code, 200)
        self.assertEqual(response_url_name.status_code, 200)

    def test_vie_give_right_context(self) -> None:
        """
        Тест представления ProfileUser на получение правильного контекста
        :return: None
        """
        view_extra_context = self.view.extra_context
        self.assertEqual(view_extra_context, {
            'title': 'Профиль пользователя',
            'default_image': settings.DEFAULT_USER_IMAGE,
        })

    def test_view_user_right_template(self) -> None:
        """
        Тест представления ProfileUser на использование правильного шаблона
        :return: None
        """
        response = self.client.get(reverse('users:profile'))
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_view_use_right_form(self) -> None:
        """
        Тест представления ProfileUser на получение правильной формы
        :return: None
        """
        view_form_class = self.view.form_class
        self.assertEqual(view_form_class, UserProfileForm)

    def test_view_use_right_model(self) -> None:
        """
        Тест представления ProfileUser на получение правильной модели
        :return: None
        """
        view_model = self.view.model
        self.assertEqual(view_model, get_user_model())

    def test_view_get_context_data(self) -> None:
        """
        Тест представления ProfileUser на получение правильного context_data
        :return: None
        """
        response = self.client.get(reverse('users:profile'))
        self.assertIn('user_orders', response.context)


