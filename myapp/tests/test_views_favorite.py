from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Playground, Favorite


class FavoriteViewsTest(TestCase):
    # テストのセットアップ
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.playground = Playground.objects.create(
            name="Test Park", address="Test Address", phone="123-456-7890"
        )
        self.add_favorite_url = reverse("add_favorite")
        self.remove_favorite_url = reverse("remove_favorite")
        self.mypage_url = reverse("mypage")

    # お気に入り追加ビューのテスト
    def test_add_favorite_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            self.add_favorite_url, {"playground_id": self.playground.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Favorite.objects.filter(user=self.user, playground=self.playground).exists()
        )

    # お気に入り削除ビューのテスト
    def test_remove_favorite_view(self):
        self.client.login(username="testuser", password="testpassword")
        Favorite.objects.create(user=self.user, playground=self.playground)
        response = self.client.post(
            self.remove_favorite_url, {"playground_id": self.playground.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Favorite.objects.filter(user=self.user, playground=self.playground).exists()
        )

    # マイページビューのテスト
    def test_mypage_view(self):
        self.client.login(username="testuser", password="testpassword")
        Favorite.objects.create(user=self.user, playground=self.playground)
        response = self.client.get(self.mypage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/mypage.html")
        self.assertEqual(len(response.context["favorites"]), 1)
