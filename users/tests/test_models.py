from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class CustomUserModelTest(TestCase):
    """
    CustomUserモデルとCustomUserManagerのテスト。
    """

    def test_create_user_with_email_and_password(self):
        """メールアドレスとパスワードでユーザーが正常に作成されることをテスト。"""
        User = get_user_model()
        email = "test@example.com"
        password = "testpassword123"
        user = User.objects.create_user(
            email=email, password=password, account_name="testuser"
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_email_raises_error(self):
        """メールアドレスなしでユーザーを作成しようとするとエラーが発生することをテスト。"""
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(
                account_name="testuser", email=None, password="testpassword123"
            )

    def test_create_user_with_empty_email_raises_error(self):
        """空のメールアドレスでユーザーを作成しようとするとエラーが発生することをテスト。"""
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(
                account_name="testuser", email="", password="testpassword123"
            )

    def test_create_superuser_with_email_and_password(self):
        """スーパーユーザーが正常に作成されることをテスト。"""
        User = get_user_model()
        email = "super@example.com"
        password = "superpassword123"
        user = User.objects.create_superuser(
            account_name="superuser", email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_superuser_must_have_is_staff_true(self):
        """スーパーユーザーはis_staff=Trueでなければならないことをテスト。"""
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                account_name="superuser",
                email="super@example.com",
                password="password",
                is_staff=False,
            )

    def test_superuser_must_have_is_superuser_true(self):
        """スーパーユーザーはis_superuser=Trueでなければならないことをテスト。"""
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                account_name="superuser",
                email="super@example.com",
                password="password",
                is_superuser=False,
            )
