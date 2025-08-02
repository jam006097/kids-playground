from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from myapp.models import Playground, Review

User = get_user_model()

class ReviewViewsTest(TestCase):
    # テストのセットアップ
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.playground = Playground.objects.create(
            name="Test Park", address="Test Address", phone="123-456-7890"
        )
        self.add_review_url = reverse(
            "myapp:add_review", kwargs={"playground_id": self.playground.id}
        )
        self.review_list_url = reverse(
            "myapp:view_reviews", kwargs={"playground_id": self.playground.id}
        )

    # レビュー追加ビューのテスト
    def test_add_review_view(self):
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.post(
            self.add_review_url, {"content": "Great park!", "rating": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Review.objects.filter(user=self.user, playground=self.playground).exists()
        )

    # レビューリストビューのテスト
    def test_review_list_view(self):
        Review.objects.create(
            user=self.user, playground=self.playground, content="Nice!", rating=4
        )
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/view_reviews.html")
        self.assertEqual(len(response.context["reviews"]), 1)
