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

    def test_mypage_displays_account_name_and_link(self):
        """マイページにアカウント名と変更ページへのリンクが表示されることをテスト"""
        response = self.client.get(reverse("accounts:mypage"))
        self.assertContains(response, self.user.account_name)
        self.assertNotContains(response, '<input type="text" name="account_name"')
        self.assertContains(response, f'href="{reverse("accounts:name_change")}"')


class AccountNameChangeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password"
        )
        self.client.login(email="testuser@example.com", password="password")
        self.url = reverse("accounts:name_change")

    def test_view_displays_form(self):
        """アカウント名変更ページにフォームが表示されることをテスト"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post"')

    def test_update_account_name(self):
        """アカウント名が更新され、マイページにリダイレクトされることをテスト"""
        new_name = "新しい名前"
        response = self.client.post(self.url, {"account_name": new_name})
        self.assertRedirects(response, reverse("accounts:mypage"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.account_name, new_name)
