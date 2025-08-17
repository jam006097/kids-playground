from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from myapp.models import Playground, Favorite

User = get_user_model()


class FavoriteViewsTest(TestCase):
    # テストのセットアップ
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.playground1 = Playground.objects.create(
            name="Test Park 1", address="Kagoshima City", phone="111-111-1111"
        )
        self.playground2 = Playground.objects.create(
            name="Test Park 2", address="Kirishima City", phone="222-222-2222"
        )
        self.add_favorite_url = reverse("myapp:add_favorite")
        self.remove_favorite_url = reverse("myapp:remove_favorite")
        self.favorites_url = reverse("myapp:favorites")

    # お気に入り追加ビューのテスト
    def test_add_favorite_view(self):
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.post(
            self.add_favorite_url, {"playground_id": self.playground1.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Favorite.objects.filter(
                user=self.user, playground=self.playground1
            ).exists()
        )

    # お気に入り削除ビューのテスト
    def test_remove_favorite_view(self):
        self.client.login(email="testuser@example.com", password="testpassword")
        Favorite.objects.create(user=self.user, playground=self.playground1)
        response = self.client.post(
            self.remove_favorite_url, {"playground_id": self.playground1.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Favorite.objects.filter(
                user=self.user, playground=self.playground1
            ).exists()
        )

    # お気に入り一覧ページのテスト
    def test_favorite_list_view(self):
        self.client.login(email="testuser@example.com", password="testpassword")
        Favorite.objects.create(user=self.user, playground=self.playground1)
        response = self.client.get(self.favorites_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favorites/list.html")
        self.assertEqual(len(response.context["favorites"]), 1)

    # お気に入り一覧ページの市町村名フィルタリングテスト
    def test_favorite_list_view_with_city_filter(self):
        self.client.login(email="testuser@example.com", password="testpassword")
        Favorite.objects.create(user=self.user, playground=self.playground1)
        Favorite.objects.create(user=self.user, playground=self.playground2)

        response = self.client.get(self.favorites_url, {"city": "Kagoshima"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favorites/list.html")
        self.assertEqual(len(response.context["favorites"]), 1)
        self.assertEqual(response.context["favorites"][0].name, "Test Park 1")
