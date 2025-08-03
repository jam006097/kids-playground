from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class MyPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password')
        self.client.login(email='testuser@example.com', password='password')

    def test_mypage_view_returns_200_for_logged_in_user(self):
        """ログイン済みのユーザーがマイページにアクセスすると200が返ってくることをテスト"""
        response = self.client.get(reverse('accounts:mypage'))
        self.assertEqual(response.status_code, 200)