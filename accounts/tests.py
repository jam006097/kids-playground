from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class MyPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password"
        )
        self.client.login(email="testuser@example.com", password="password")

    def test_mypage_view_returns_200_for_logged_in_user(self):
        """ログイン済みのユーザーがマイページにアクセスすると200が返ってくることをテスト"""
        response = self.client.get(reverse("accounts:mypage"))
        self.assertEqual(response.status_code, 200)

    def test_email_management_page_returns_200_for_logged_in_user(self):
        """ログイン済みのユーザーがメールアドレス管理ページにアクセスすると200が返ってくることをテスト"""
        response = self.client.get(reverse("account_email"))
        self.assertEqual(response.status_code, 200)

    def test_email_management_page_contains_correct_title(self):
        """メールアドレス管理ページに正しいタイトルが表示されることをテスト"""
        response = self.client.get(reverse("account_email"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "メールアドレスの管理")
