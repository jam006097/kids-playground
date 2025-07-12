from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Playground, Review


class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.playground = Playground.objects.create(
            name="Test Park", address="Test Address", phone="123-456-7890"
        )
        self.add_review_url = reverse(
            "add_review", kwargs={"playground_id": self.playground.id}
        )
        self.review_list_url = reverse(
            "view_reviews", kwargs={"playground_id": self.playground.id}
        )

    def test_add_review_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            self.add_review_url, {"content": "Great park!", "rating": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Review.objects.filter(user=self.user, playground=self.playground).exists()
        )

    def test_review_list_view(self):
        Review.objects.create(
            user=self.user, playground=self.playground, content="Nice!", rating=4
        )
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_reviews.html")
        self.assertEqual(len(response.context["reviews"]), 1)
