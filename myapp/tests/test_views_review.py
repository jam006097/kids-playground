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
            email="testuser@example.com",
            password="testpassword",
            account_name="testuser",
        )
        self.playground = Playground.objects.create(
            name="Test Park", address="Test Address", phone="123-456-7890"
        )
        self.add_review_url = reverse(
            "myapp:add_review", kwargs={"playground_id": self.playground.id}
        )

    def test_add_review_returns_created_review_json(self):
        """
        レビューを正常に投稿すると、作成されたレビューのJSONが返されることをテストする。
        """
        self.client.login(email="testuser@example.com", password="testpassword")
        post_data = {"content": "Great park!", "rating": 5}
        response = self.client.post(self.add_review_url, post_data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response_data = response.json()
        self.assertEqual(response_data["status"], "success")

        self.assertIn("review", response_data)
        review_data = response_data["review"]

        self.assertEqual(review_data["content"], post_data["content"])
        self.assertEqual(review_data["rating"], post_data["rating"])
        self.assertEqual(review_data["user_account_name"], self.user.account_name)

        # Check if review exists in DB as a sanity check
        self.assertTrue(
            Review.objects.filter(
                user=self.user,
                playground=self.playground,
                content=post_data["content"],
            ).exists()
        )

    def test_add_review_view_invalid_rating(self):
        """不正なratingでレビュー追加を試みると400エラーが返ることをテスト"""
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.post(
            self.add_review_url, {"content": "Great park!", "rating": "abc"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid rating")
