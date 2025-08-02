from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from myapp.models import Playground, Favorite

User = get_user_model()

class TemplateRenderTest(TestCase):
    def setUp(self):
        """テスト用のデータを作成"""
        self.user = User.objects.create_user(email="testuser@example.com", password="password")
        self.playground1 = Playground.objects.create(
            name="Test Park 1", address="Address 1"
        )
        self.playground2 = Playground.objects.create(
            name="Test Park 2", address="Address 2"
        )
        # playground1をお気に入りに追加
        Favorite.objects.create(user=self.user, playground=self.playground1)

    def test_favorite_button_display_logic(self):
        """
        お気に入り状態に応じてボタンのテキストが正しく表示されるかテスト
        """
        self.client.login(email="testuser@example.com", password="password")
        response = self.client.get(reverse("myapp:index"))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")

        # playground1（お気に入り済み）のボタンを確認
        button1 = soup.find("button", {"data-playground-id": self.playground1.id})
        self.assertIn("お気に入り解除", button1.text)

        # playground2（お気に入り未登録）のボタンを確認
        button2 = soup.find("button", {"data-playground-id": self.playground2.id})
        self.assertIn("お気に入りに追加", button2.text)

    def test_favorite_button_disabled_for_anonymous_user(self):
        """
        未ログインユーザーにはお気に入りボタンが無効化されているかテスト
        """
        response = self.client.get(reverse("myapp:index"))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")

        # playground1のボタンが無効化されているか確認
        button1 = soup.find("button", {"data-playground-id": self.playground1.id})
        self.assertIsNotNone(button1, "ボタンが見つかりません")
        self.assertTrue(button1.has_attr("disabled"), "disabled属性がありません")
        self.assertEqual(button1.get("title"), "ログインするとお気に入り機能が使えます")
