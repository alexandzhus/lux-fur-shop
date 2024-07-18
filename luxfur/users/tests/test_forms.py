import shutil

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from config import settings
from users.forms import LoginUserForm, UserProfileForm, UserRegisterForm
import tempfile
from django.test import TestCase, Client, override_settings

# Создаем временную папку для хранения меда файлов.
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR / 'media')


# Для сохранения media-файлов в тестах будет использоваться
# временная папка TEMP_MEDIA_ROOT, после временная папка удаляется

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UserProfileFormCase(TestCase):
    """
    Тестируем форму для редактирования профиля пользователя
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = get_user_model().objects.create(username='sashadzhus',
                                                        email='alexandrdzhus@gmail.com',
                                                        password='123',
                                                        )

        cls.profile_form = UserProfileForm()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B')

        avatar = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        cls.form_data = {'avatar': avatar,
                         'first_name': 'Александр',
                         'last_name': 'Александр'
                         }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()
        # Модуль shutil - библиотека Python с удобными инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение, изменение папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        """
        Метод применяется перед запуском каждого теста. Создается тестовый неавторизованный клиент
        :return: None
        """
        self.client.force_login(self.test_user)

    def test_update_user_profile(self) -> None:
        """
        Тест на обновления профиля пользователя. Проверка на сохранение аватарки, имени и фамилии.
        :return: None
        """
        task_count = get_user_model().objects.count()

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)

        response2 = self.client.post(reverse('users:profile'), data=self.form_data, follow=True)
        # Проверяем выполнился-ли redirect
        self.assertRedirects(response2, reverse('users:profile'))
        # Сохраняем изменения в базе данных
        self.test_user.refresh_from_db()
        # Проверяем есть ли у пользователя аватар, имя и фамилия
        self.assertTrue(self.test_user.avatar)
        self.assertTrue(self.test_user.first_name)
        self.assertTrue(self.test_user.last_name)

        self.assertEqual(task_count, get_user_model().objects.count())

    # def test_update_user_profile_first_name(self) -> None:
    #     """
    #     Тест на обновления профиля пользователя. Проверка на сохранение Имени пользователя.
    #     :return: None
    #     """
    #
    #     response = self.client.post(reverse('users:profile'), data=form_data, follow=True)
    #     self.assertRedirects(response, reverse('users:profile'))
    #     # сохраняем изменения в базе
    #     self.test_user.refresh_from_db()
    #     # Проверяем, что у пользователя есть имя
    #     self.assertTrue(self.test_user.first_name)
    #
    # def test_update_user_profile_last_name(self) -> None:
    #     """
    #     Тест на обновления профиля пользователя. Проверка на сохранение Фамилии пользователя.
    #     :return: None
    #     """
    #
    #     response = self.client.post(reverse('users:profile'), data=form_data, follow=True)
    #     self.assertRedirects(response, reverse('users:profile'))
    #     self.test_user.refresh_from_db()
    #     # Проверяем, что у пользователя есть фамилии
    #     self.assertTrue(self.test_user.last_name)

    def test_profile_form_username_label(self) -> None:
        """
        Тестируем поле username формы UserProfileForm на свойство label
        :return: None
        """
        profile_form = UserProfileForm()
        self.assertTrue(
            profile_form.fields['username'].label == None or profile_form.fields['username'].label == 'Логин')

    def test_profile_form_username_disabled(self) -> None:
        """
        Тестируем поле username формы UserProfileForm на свойство disabled
        :return: None
        """
        profile_form = UserProfileForm()
        self.assertTrue(profile_form.fields['username'].disabled)

    def test_profile_form_email_label(self) -> None:
        """
        Тестируем поле email формы UserProfileForm на свойство label
        :return: None
        """
        profile_form = UserProfileForm()
        self.assertTrue(
            profile_form.fields['email'].label == None or profile_form.fields['email'].label == 'E-mail')

    def test_profile_form_email_disabled(self) -> None:
        """
        Тестируем поле email формы UserProfileForm на свойство disabled
        :return: None
        """
        profile_form = UserProfileForm()
        self.assertTrue(profile_form.fields['email'].disabled)

    def test_profile_form_avatar_label(self) -> None:
        """
        Тестируем поле avatar формы UserProfileForm на свойство label
        :return: None
        """
        profile_form = UserProfileForm()
        self.assertTrue(
            profile_form.fields['avatar'].label == None or profile_form.fields['avatar'].label == 'Аватар пользователя')

    def test_profile_form_first_name_label(self) -> None:
        """
        Тестируем поле first_name формы UserProfileForm на свойство label
        :return: None
        """
        profile_form = UserProfileForm()
        self.assertEqual(profile_form.fields['first_name'].label, 'Имя')

    def test_profile_form_last_name_label(self) -> None:
        """
        Тестируем поле last_name формы UserProfileForm на свойство label
        :return: None
        """
        profile_form = UserProfileForm()
        self.assertEqual(profile_form.fields['last_name'].label, 'Фамилия')


class LoginUserFormCase(TestCase):
    """
    Тестируем форму для аутентификации пользователя
    """

    def test_login_form_username_max_length(self) -> None:
        """
        Тестируем поле username формы LoginUserForm на свойство max_length
        :return: None
        """
        login_form = LoginUserForm()
        self.assertEqual(login_form.fields['username'].max_length, 150)

    def test_login_form_username_label(self) -> None:
        """
        Тестируем поле username формы LoginUserForm на свойство label
        :return: None
        """
        login_form = LoginUserForm()
        self.assertEqual(login_form.fields['username'].label, 'Логин')

    def test_login_form_password_label(self) -> None:
        """
        Тестируем поле password формы LoginUserForm на свойство label
        :return: None
        """
        login_form = LoginUserForm()
        self.assertEqual(login_form.fields['password'].label, 'Пароль')


class UserRegisterFormCase(TestCase):
    """
    Тестируем форму для регистрации пользователя
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.register_form = UserRegisterForm()
        cls.new_user = get_user_model().objects.create(username='sashadzhus',
                                                       email='alexandrdzhus@gmail.com',
                                                       password='dzhus1234567',
                                                       )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.new_user.delete()

    def test_register_form_username_label(self) -> None:
        """
        Тестируем поле username формы UserRegisterForm на свойство label
        :return: None
        """
        self.assertEqual(self.register_form.fields['username'].label, 'Логин')

    def test_register_form_password1_label(self) -> None:
        """
        Тестируем поле password1 формы UserRegisterForm на свойство label
        :return: None
        """
        self.assertEqual(self.register_form.fields['password1'].label, 'Пароль')

    def test_register_form_password2_label(self) -> None:
        """
        Тестируем поле password2 формы UserRegisterForm на свойство label
        :return: None
        """
        self.assertEqual(self.register_form.fields['password2'].label, 'Повторите пароль')

    def test_register_form_email_label(self) -> None:
        """
        Тестируем поле email формы UserRegisterForm на свойство label
        :return: None
        """
        self.assertEqual(self.register_form.fields['email'].label, 'E-mail')

    def test_register_form_first_name_label(self) -> None:
        """
        Тестируем поле first_name формы UserRegisterForm на свойство label
        :return: None
        """
        self.assertEqual(self.register_form.fields['first_name'].label, 'Имя')

    def test_register_form_last_name_label(self) -> None:
        """
        Тестируем поле last_name формы UserRegisterForm на свойство label
        :return: None
        """
        self.assertEqual(self.register_form.fields['last_name'].label, 'Фамилия')

    def test_register_form_clean_email_field(self) -> None:
        """
        Тестируем форму UserRegisterForm поле email. Проверяем является ли введенный эмейл уникальным(False).
        :return: None
        """
        data = {'username': 'sashadzhus',
                'email': 'alexandrdzhus@gmail.com',
                'first_name': 'sasha',
                'last_name': 'dzhus',
                'password1': 'dzhus1234567',
                'password2': 'dzhus1234567',
                }

        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_register_form_clean_email_field_true(self) -> None:
        """
        Тестируем форму UserRegisterForm поле email. Подтверждение, что такого эмейла в базе не существует(True).
        :return: None
        """
        data = {'username': 'sashadzhus1',
                'email': 'alexandrdzhus1@gmail.com',
                'first_name': 'sasha1',
                'last_name': 'dzhus1',
                'password1': 'dzhus12345671',
                'password2': 'dzhus12345671',
                }

        form = UserRegisterForm(data=data)
        self.assertTrue(form.is_valid())
